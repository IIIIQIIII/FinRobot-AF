"""
Forward-Looking Statement (FLS) Extraction Workflow
====================================================

Extract FLS from 10-K filings using workflow configuration.

Configuration file: config/workflows/fls_extraction.json

This workflow:
1. Loads 10-K filing from data folder
2. Extracts FLS from Section 7 (MD&A) using FLS_MDA_Analyst
3. Extracts FLS from Section 1A (Risk Factors) using FLS_Risk_Analyst
4. Saves structured results with categorization

Usage:
    python examples/fls_workflow.py
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from finrobot.workflow_config import WorkflowConfig
from finrobot.llm_config import switch_provider
from finrobot.config import FinRobotConfig
from finrobot.agents.agent_library import create_agent
from finrobot.functional.fls_detection import analyze_fls_in_text


async def extract_fls_from_section(
    section_text: str,
    section_name: str,
    agent_name: str,
    llm_config: dict,
    metadata: dict
) -> dict:
    """
    Extract FLS from a section using configured agent.

    Args:
        section_text: Text of the section
        section_name: Name of section (e.g., "Section 7 - MD&A")
        agent_name: Agent to use (FLS_MDA_Analyst or FLS_Risk_Analyst)
        llm_config: LLM configuration for this step
        metadata: Filing metadata

    Returns:
        Dictionary with FLS extraction results
    """
    print(f"{'='*80}")
    print(f"FLS EXTRACTION: {section_name}")
    print(f"{'='*80}")
    print(f"Provider: {llm_config['provider']}")
    print(f"Model: {llm_config['model']}")
    print(f"Temperature: {llm_config['temperature']}")
    print(f"Agent: {agent_name}")
    print(f"Text length: {len(section_text):,} chars\n")

    # Switch to configured LLM
    switch_provider(llm_config['provider'], llm_config['model'])

    # Get config and create agent
    config = FinRobotConfig()
    chat_client = config.get_chat_client()
    agent = create_agent(agent_name, chat_client)

    # Pre-analysis with signal word detection
    preliminary_analysis = analyze_fls_in_text(
        section_text,
        section_name=section_name,
        min_confidence=0.5
    )

    print(f"Preliminary analysis: {preliminary_analysis['total_fls_found']} FLS candidates detected")
    print(f"Running {agent_name} for deep analysis...\n")

    # Prepare prompt
    prompt = f"""
Analyze the following {section_name} text and extract Forward-Looking Statements (FLS).

FILING METADATA:
- CIK: {metadata['cik']}
- Year: {metadata['year']}
- Text Length: {len(section_text):,} characters

PRELIMINARY ANALYSIS:
- Potential FLS segments detected: {preliminary_analysis['total_fls_found']}
- Signal categories: {', '.join(preliminary_analysis['signal_categories'].keys())}

TEXT:
{section_text}

TASK:
Extract all Forward-Looking Statements from the text above. For each FLS:
1. Provide the complete text (full sentences/paragraphs)
2. Identify FLS signal words
3. Classify the FLS category
4. Rate your confidence (0.0-1.0)
5. Explain your reasoning

Output as JSON following the format specified in your instructions.
"""

    # Run agent
    response = await agent.run(prompt)

    # Parse JSON response
    try:
        response_text = response.text if hasattr(response, 'text') else str(response)
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx != -1 and end_idx > start_idx:
            json_text = response_text[start_idx:end_idx]
            extraction_result = json.loads(json_text)
        else:
            # Fallback to preliminary analysis
            extraction_result = {
                "fls_segments": preliminary_analysis["fls_segments"],
                "summary": "Automated extraction using signal word detection",
                "statistics": preliminary_analysis
            }
    except json.JSONDecodeError:
        print("⚠ Warning: Could not parse JSON from agent, using preliminary analysis")
        extraction_result = {
            "fls_segments": preliminary_analysis["fls_segments"],
            "summary": "Automated extraction using signal word detection",
            "statistics": preliminary_analysis
        }

    fls_count = len(extraction_result.get('fls_segments', []))
    print(f"✓ Extracted {fls_count} FLS segments\n")

    return extraction_result


async def run_fls_extraction(cik: str, year: str):
    """
    Run FLS extraction workflow on a 10-K filing.

    Args:
        cik: Company CIK number
        year: Filing year

    Returns:
        Path to output file
    """
    # Load workflow configuration
    workflow_config = WorkflowConfig("fls_extraction")
    paths = workflow_config.get_paths()
    options = workflow_config.get_options()

    # Ensure output directory exists
    paths["output_folder"].mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"FLS EXTRACTION WORKFLOW: {cik} ({year})")
    print(f"{'='*80}\n")

    # Load filing
    input_file = paths["input_folder"] / f"{cik}_{year}.json"
    if not input_file.exists():
        raise FileNotFoundError(f"Filing not found: {input_file}")

    with open(input_file) as f:
        data = json.load(f)

    # Extract sections
    section_7 = data.get('section_7', '')
    section_1a = data.get('section_1A', '')

    if not section_7:
        raise ValueError(f"No Section 7 (MD&A) found in filing")

    metadata = {
        'cik': cik,
        'year': year,
        'company_name': data.get('company_name', 'Unknown'),
        'section_7_length': len(section_7),
        'section_1a_length': len(section_1a),
        'filing_date': data.get('filing_date', '')
    }

    print(f"Company: {metadata['company_name']}")
    print(f"Filing: {cik} - {year}")
    print(f"Section 7 length: {metadata['section_7_length']:,} chars")
    print(f"Section 1A length: {metadata['section_1a_length']:,} chars\n")

    # Extract from Section 7 (MD&A)
    mda_config = workflow_config.get_llm_config("mda_fls_extraction")
    mda_results = await extract_fls_from_section(
        section_7,
        "Section 7 - MD&A",
        mda_config['agent_name'],
        mda_config,
        metadata
    )

    # Extract from Section 1A (Risk Factors)
    risk_results = {"fls_segments": [], "summary": "Section not available"}
    if section_1a:
        risk_config = workflow_config.get_llm_config("risk_fls_extraction")
        risk_results = await extract_fls_from_section(
            section_1a,
            "Section 1A - Risk Factors",
            risk_config['agent_name'],
            risk_config,
            metadata
        )

    # Combine results
    combined_result = {
        "metadata": {
            **metadata,
            "extraction_timestamp": datetime.now().isoformat(),
            "workflow": workflow_config.workflow_name
        },
        "section_7_mda": {
            "fls_count": len(mda_results.get('fls_segments', [])),
            "summary": mda_results.get('summary', ''),
            "fls_segments": mda_results.get('fls_segments', [])
        },
        "section_1a_risks": {
            "fls_count": len(risk_results.get('fls_segments', [])),
            "summary": risk_results.get('summary', ''),
            "fls_segments": risk_results.get('fls_segments', [])
        },
        "combined_statistics": {
            "total_fls_extracted": (
                len(mda_results.get('fls_segments', [])) +
                len(risk_results.get('fls_segments', []))
            ),
            "mda_fls": len(mda_results.get('fls_segments', [])),
            "risk_fls": len(risk_results.get('fls_segments', []))
        }
    }

    # Save results
    output_file = paths["output_folder"] / f"fls_{cik}_{year}.json"
    with open(output_file, 'w') as f:
        json.dump(combined_result, f, indent=2)

    print(f"{'='*80}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Section 7 (MD&A): {combined_result['section_7_mda']['fls_count']} FLS")
    print(f"Section 1A (Risk): {combined_result['section_1a_risks']['fls_count']} FLS")
    print(f"Total FLS: {combined_result['combined_statistics']['total_fls_extracted']}")
    print(f"\n✓ Results saved to: {output_file}\n")

    return output_file


async def main():
    """Run FLS extraction on example filing."""

    # Example: Extract FLS from Abbott Laboratories 2020 10-K
    output_file = await run_fls_extraction("1800", "2020")

    print("✓ FLS extraction complete!")
    print(f"  Output: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
