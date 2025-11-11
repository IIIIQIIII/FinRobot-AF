"""
FLS Pipeline: Agent-based Forward-Looking Statement extraction workflow.
Implements multi-agent pipeline for analyzing 10-K Section 7 and Section 1A.
"""

import asyncio
import json
from typing import Dict, Optional

from finrobot.agents.agent_library import create_agent
from finrobot.config import FinRobotConfig


class FLSPipeline:
    """
    Sequential pipeline for FLS extraction from 10-K filings.

    Architecture:
        10-K Sections → FLS_MDA_Analyst (Section 7) → Results
                     → FLS_Risk_Analyst (Section 1A) → Results

    The pipeline uses two specialized agents:
    1. FLS_MDA_Analyst: Extracts FLS from Section 7 (MD&A)
    2. FLS_Risk_Analyst: Extracts FLS from Section 1A (Risk Factors)
    """

    def __init__(self, config: Optional[FinRobotConfig] = None):
        """
        Initialize FLS pipeline.

        Args:
            config: FinRobot configuration. If None, loads default config.
        """
        if config is None:
            config = FinRobotConfig()

        self.config = config
        self.chat_client = config.get_chat_client()

        # Create specialized FLS agents
        self.mda_analyst = create_agent(
            "FLS_MDA_Analyst",
            self.chat_client,
            toolkit_registry=None
        )

        self.risk_analyst = create_agent(
            "FLS_Risk_Analyst",
            self.chat_client,
            toolkit_registry=None
        )

    async def extract_fls_from_mda(self, section_7_text: str, metadata: Dict) -> Dict:
        """
        Extract FLS from Section 7 (MD&A).

        Args:
            section_7_text: Full Section 7 text
            metadata: Filing metadata (cik, year, etc.)

        Returns:
            Dictionary containing FLS extraction results
        """
        print(f"\n{'='*80}")
        print(f"FLS EXTRACTION (MD&A): {metadata['cik']} ({metadata['year']})")
        print(f"{'='*80}")
        print(f"Section 7 length: {len(section_7_text)} chars (~{len(section_7_text.split())} words)")

        # Create extraction prompt
        prompt = f"""Analyze the following Section 7 (Management's Discussion & Analysis) from a 10-K filing.

Extract ALL Forward-Looking Statements (FLS) - statements that project, anticipate, or discuss future events, plans, expectations, or outcomes.

Key FLS Signal Words:
- Planning: anticipates, intends, plans, seeks
- Expectations: expects, believes, guidance, outlook
- Possibility: could, may, might, potential
- Projections: estimates, projects, forecasts
- Likelihood: should, will, would, likely

FLS Categories for MD&A:
1. revenue_guidance - Revenue/earnings projections
2. strategic - Strategic initiatives and plans
3. market_outlook - Market expectations
4. operational - Operational improvements
5. capital - Capital allocation plans
6. risk_mitigation - Risk mitigation strategies

Return your analysis in JSON format as specified in your instructions.

--- SECTION 7 TEXT ---
{section_7_text}
--- END SECTION 7 TEXT ---
"""

        print("\n⏳ Running FLS_MDA_Analyst agent...")

        # Run FLS extraction agent
        result = await self.mda_analyst.run(
            messages=prompt,
            temperature=0.3  # Lower temperature for consistency
        )

        # Extract text from result
        if hasattr(result, 'text'):
            response_text = result.text
        elif isinstance(result, str):
            response_text = result
        else:
            response_text = str(result)

        print(f"✓ Agent response received ({len(response_text)} chars)")

        # Parse JSON from response
        try:
            # Try to find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                extraction_result = json.loads(json_text)

                # Add metadata
                extraction_result['metadata'] = metadata
                extraction_result['section'] = 'Section 7 - MD&A'

                segments = extraction_result.get('fls_segments', [])
                print(f"✓ Extracted {len(segments)} FLS segments from MD&A")

                return extraction_result
            else:
                print("⚠ No JSON found in response, returning raw text")
                return {
                    'fls_segments': [],
                    'summary': response_text[:500],
                    'metadata': metadata,
                    'section': 'Section 7 - MD&A',
                    'error': 'JSON parsing failed'
                }

        except json.JSONDecodeError as e:
            print(f"⚠ JSON decode error: {e}")
            return {
                'fls_segments': [],
                'summary': response_text[:500],
                'metadata': metadata,
                'section': 'Section 7 - MD&A',
                'error': str(e)
            }

    async def extract_fls_from_risks(self, section_1a_text: str, metadata: Dict) -> Dict:
        """
        Extract FLS from Section 1A (Risk Factors).

        Args:
            section_1a_text: Full Section 1A text
            metadata: Filing metadata (cik, year, etc.)

        Returns:
            Dictionary containing FLS extraction results
        """
        print(f"\n{'='*80}")
        print(f"FLS EXTRACTION (RISKS): {metadata['cik']} ({metadata['year']})")
        print(f"{'='*80}")
        print(f"Section 1A length: {len(section_1a_text)} chars (~{len(section_1a_text.split())} words)")

        # Create extraction prompt
        prompt = f"""Analyze the following Section 1A (Risk Factors) from a 10-K filing.

Extract ALL Forward-Looking Statements (FLS) - statements describing potential future events and their impacts.

Risk Factors are inherently forward-looking. Focus on:
- Hypothetical future events (could, may, might, would)
- Projected impacts of risks
- Conditional statements about future outcomes

FLS Categories for Risk Factors:
1. market - Market and competitive risks
2. operational - Operational risks
3. financial - Financial risks
4. regulatory - Regulatory and legal risks
5. strategic - Strategic execution risks
6. external - Geopolitical, economic, environmental risks

Return your analysis in JSON format as specified in your instructions.

--- SECTION 1A TEXT ---
{section_1a_text}
--- END SECTION 1A TEXT ---
"""

        print("\n⏳ Running FLS_Risk_Analyst agent...")

        # Run FLS extraction agent
        result = await self.risk_analyst.run(
            messages=prompt,
            temperature=0.3
        )

        # Extract text from result
        if hasattr(result, 'text'):
            response_text = result.text
        elif isinstance(result, str):
            response_text = result
        else:
            response_text = str(result)

        print(f"✓ Agent response received ({len(response_text)} chars)")

        # Parse JSON from response
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                extraction_result = json.loads(json_text)

                extraction_result['metadata'] = metadata
                extraction_result['section'] = 'Section 1A - Risk Factors'

                segments = extraction_result.get('fls_segments', [])
                print(f"✓ Extracted {len(segments)} FLS segments from Risk Factors")

                return extraction_result
            else:
                print("⚠ No JSON found in response")
                return {
                    'fls_segments': [],
                    'summary': response_text[:500],
                    'metadata': metadata,
                    'section': 'Section 1A - Risk Factors',
                    'error': 'JSON parsing failed'
                }

        except json.JSONDecodeError as e:
            print(f"⚠ JSON decode error: {e}")
            return {
                'fls_segments': [],
                'summary': response_text[:500],
                'metadata': metadata,
                'section': 'Section 1A - Risk Factors',
                'error': str(e)
            }

    async def extract_fls(self, section_7: str, section_1a: str, metadata: Dict) -> Dict:
        """
        Extract FLS from both Section 7 and Section 1A.

        Args:
            section_7: Section 7 (MD&A) text
            section_1a: Section 1A (Risk Factors) text
            metadata: Filing metadata

        Returns:
            Combined results from both sections
        """
        # Extract from both sections in parallel
        mda_task = self.extract_fls_from_mda(section_7, metadata)
        risk_task = self.extract_fls_from_risks(section_1a, metadata)

        mda_result, risk_result = await asyncio.gather(mda_task, risk_task)

        # Combine results
        return {
            'section_7_mda': mda_result,
            'section_1a_risks': risk_result,
            'combined_statistics': {
                'mda_fls': len(mda_result.get('fls_segments', [])),
                'risk_fls': len(risk_result.get('fls_segments', [])),
                'total_fls': (
                    len(mda_result.get('fls_segments', [])) +
                    len(risk_result.get('fls_segments', []))
                )
            }
        }
