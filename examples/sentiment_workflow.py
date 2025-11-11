"""
Sentiment Analysis Workflow
============================

Run sentiment analysis on 10-K filings using workflow configuration.

Configuration file: config/workflows/sentiment_analysis.json

This workflow:
1. Loads 10-K filing from data folder
2. Extracts policy discussions (using Policy_Analyst agent)
3. Analyzes sentiment (using Sentiment_Analyst agent)
4. Saves structured results

Usage:
    python examples/sentiment_workflow.py
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from finrobot.workflow_config import WorkflowConfig
from finrobot.llm_config import switch_provider
from finrobot.workflows.finagent_pipeline import FinAgentPipeline
from finrobot.config import FinRobotConfig


async def run_sentiment_analysis(cik: str, year: str):
    """
    Run sentiment analysis workflow on a 10-K filing.

    Args:
        cik: Company CIK number
        year: Filing year

    Returns:
        Path to output file
    """
    # Load workflow configuration
    workflow_config = WorkflowConfig("sentiment_analysis")
    paths = workflow_config.get_paths()
    options = workflow_config.get_options()

    # Ensure output directory exists
    paths["output_folder"].mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"SENTIMENT ANALYSIS WORKFLOW: {cik} ({year})")
    print(f"{'='*80}\n")

    # Load filing
    input_file = paths["input_folder"] / f"{cik}_{year}.json"
    if not input_file.exists():
        raise FileNotFoundError(f"Filing not found: {input_file}")

    with open(input_file) as f:
        data = json.load(f)

    # Get Item 7 text
    item7_text = data.get('item7_mda') or data.get('section_7') or ''
    if not item7_text:
        raise ValueError(f"No Item 7 (MD&A) found in filing")

    metadata = {
        'cik': cik,
        'year': year,
        'company_name': data.get('company_name', 'Unknown'),
        'word_count': len(item7_text.split()),
        'filing_date': data.get('filing_date', '')
    }

    print(f"Company: {metadata['company_name']}")
    print(f"Filing: {cik} - {year}")
    print(f"Item 7 length: {metadata['word_count']:,} words\n")

    # Initialize pipeline
    config = FinRobotConfig()
    pipeline = FinAgentPipeline(config)

    # Step 1: Extract policy discussions
    extraction_config = workflow_config.get_llm_config("extraction")

    print(f"{'='*80}")
    print(f"STEP 1: Policy Extraction")
    print(f"{'='*80}")
    print(f"Provider: {extraction_config['provider']}")
    print(f"Model: {extraction_config['model']}")
    print(f"Temperature: {extraction_config['temperature']}")
    print(f"Agent: {extraction_config['agent_name']}\n")

    switch_provider(extraction_config['provider'], extraction_config['model'])
    extraction_result = await pipeline.extract_policies(item7_text, metadata)

    print(f"✓ Extracted {len(extraction_result.get('segments', []))} policy segments\n")

    # Step 2: Analyze sentiment
    sentiment_config = workflow_config.get_llm_config("sentiment")

    print(f"{'='*80}")
    print(f"STEP 2: Sentiment Analysis")
    print(f"{'='*80}")
    print(f"Provider: {sentiment_config['provider']}")
    print(f"Model: {sentiment_config['model']}")
    print(f"Temperature: {sentiment_config['temperature']}")
    print(f"Agent: {sentiment_config['agent_name']}\n")

    switch_provider(sentiment_config['provider'], sentiment_config['model'])
    sentiment_result = await pipeline.analyze_sentiment(extraction_result, metadata)

    overall_sentiment = sentiment_result.get('overall_sentiment', 'unknown')
    sentiment_score = sentiment_result.get('sentiment_score', 0.0)

    print(f"✓ Overall sentiment: {overall_sentiment}")
    print(f"✓ Sentiment score: {sentiment_score:+.2f}\n")

    # Combine results
    combined_result = {
        "metadata": {
            **metadata,
            "analysis_timestamp": datetime.now().isoformat(),
            "workflow": workflow_config.workflow_name
        },
        "extraction": extraction_result,
        "sentiment": sentiment_result,
        "summary": {
            "total_segments": len(extraction_result.get('segments', [])),
            "overall_sentiment": overall_sentiment,
            "sentiment_score": sentiment_score
        }
    }

    # Save results
    output_file = paths["output_folder"] / f"sentiment_{cik}_{year}.json"
    with open(output_file, 'w') as f:
        json.dump(combined_result, f, indent=2)

    print(f"{'='*80}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Policy segments: {combined_result['summary']['total_segments']}")
    print(f"Overall sentiment: {combined_result['summary']['overall_sentiment']}")
    print(f"Sentiment score: {combined_result['summary']['sentiment_score']:+.2f}")
    print(f"\n✓ Results saved to: {output_file}\n")

    return output_file


async def main():
    """Run sentiment analysis on example filing."""

    # Example: Analyze Abbott Laboratories 2020 10-K
    output_file = await run_sentiment_analysis("1800", "2020")

    print("✓ Sentiment analysis complete!")
    print(f"  Output: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
