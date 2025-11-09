"""
FinAgent Pipeline: Sequential extraction and sentiment analysis workflow.
Implements multi-agent pipeline for analyzing 10-K Item 7 sections.
"""

import asyncio
import json
from typing import Dict, Tuple, Optional

from finrobot.agents.agent_library import create_agent
from finrobot.config import FinRobotConfig
from finrobot.utils.data_loader import ResultWriter


class FinAgentPipeline:
    """
    Sequential pipeline for policy extraction and sentiment analysis.

    Architecture:
        10-K Item 7 Text → Policy_Extractor → Sentiment_Analyzer → Results

    The pipeline uses two specialized agents:
    1. Policy_Extractor: Identifies and extracts macroeconomic policy discussions
    2. Sentiment_Analyzer: Classifies sentiment of extracted text (optimistic/pessimistic)
    """

    def __init__(self, config: Optional[FinRobotConfig] = None):
        """
        Initialize FinAgent pipeline.

        Args:
            config: FinRobot configuration. If None, loads default config.
        """
        if config is None:
            config = FinRobotConfig()

        self.config = config
        self.chat_client = config.get_chat_client()
        self.result_writer = ResultWriter()

        # Create specialized agents
        self.extractor = create_agent(
            "Policy_Extractor",
            self.chat_client,
            toolkit_registry=None  # No tools needed for text analysis
        )

        self.sentiment_analyzer = create_agent(
            "Sentiment_Analyzer",
            self.chat_client,
            toolkit_registry=None
        )

    async def extract_policies(self, item7_text: str, metadata: Dict) -> Dict:
        """
        Extract macroeconomic policy discussions from Item 7 text.

        Args:
            item7_text: Full Item 7 (MD&A) text
            metadata: Filing metadata (cik, year, etc.)

        Returns:
            Dictionary containing extraction results
        """
        print(f"\n{'='*80}")
        print(f"POLICY EXTRACTION: {metadata['cik']} ({metadata['year']})")
        print(f"{'='*80}")
        print(f"Item 7 length: {len(item7_text)} chars (~{len(item7_text.split())} words)")

        # Create extraction prompt
        prompt = f"""Please analyze the following Item 7 (Management's Discussion & Analysis) section from a 10-K filing.

Extract ALL text segments that discuss macroeconomic policies and their impacts on the company.

Focus on these policy types:
1. Monetary policy (Federal Reserve, interest rates)
2. Fiscal policy (government spending, stimulus)
3. Trade policy (tariffs, trade agreements)
4. Tax policy (tax rates, tax reform)
5. Regulatory policy (regulations, compliance)

Return your analysis in JSON format as specified in your instructions.

--- ITEM 7 TEXT ---
{item7_text}
--- END ITEM 7 TEXT ---
"""

        print("\n⏳ Running Policy_Extractor agent...")

        # Run extraction agent
        result = await self.extractor.run(
            messages=prompt,
            temperature=0.0  # Deterministic output for consistency
        )

        # Extract text from result
        if hasattr(result, 'text'):
            response_text = result.text
        elif isinstance(result, str):
            response_text = result
        else:
            response_text = str(result)

        print(f"\n✓ Extraction completed")
        print(f"Response length: {len(response_text)} chars")

        # Try to parse JSON from response
        try:
            # Look for JSON in response (might be wrapped in markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                # Try to extract JSON object
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text

            extraction_data = json.loads(json_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, create structured response
            print("⚠️  JSON parsing failed, using fallback structure")
            extraction_data = {
                "extracted_segments": [],
                "summary": "Could not parse extraction results",
                "raw_response": response_text[:1000],  # Store first 1000 chars
                "error": "JSON parsing failed"
            }

        # Add metadata
        extraction_data['metadata'] = metadata
        extraction_data['model'] = getattr(self.chat_client, 'model_id', 'unknown')

        return extraction_data

    async def analyze_sentiment(self, extraction_data: Dict, metadata: Dict) -> Dict:
        """
        Analyze sentiment of extracted policy discussions.

        Args:
            extraction_data: Results from policy extraction
            metadata: Filing metadata

        Returns:
            Dictionary containing sentiment analysis results
        """
        print(f"\n{'='*80}")
        print(f"SENTIMENT ANALYSIS: {metadata['cik']} ({metadata['year']})")
        print(f"{'='*80}")

        # Check if extraction was successful
        if not extraction_data.get('extracted_segments'):
            print("⚠️  No policy segments extracted, skipping sentiment analysis")
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0.0,
                'confidence': 0.0,
                'reasoning': 'No policy segments found for analysis',
                'segment_sentiments': [],
                'metadata': metadata,
                'model': self.chat_client.model
            }

        # Format extracted segments for sentiment analysis
        segments_text = "\n\n".join([
            f"Segment {seg['segment_id']}: {seg['text']}"
            for seg in extraction_data.get('extracted_segments', [])
        ])

        # Create sentiment analysis prompt
        prompt = f"""Analyze the sentiment of the following text segments extracted from a 10-K Item 7 section.

These segments discuss macroeconomic policies. Classify the overall management sentiment as:
- OPTIMISTIC (+1.0): Positive outlook, opportunities, benefits
- PESSIMISTIC (-1.0): Concerns, challenges, negative impacts
- NEUTRAL (0.0): Balanced or uncertain

Return your analysis in JSON format as specified in your instructions.

--- EXTRACTED POLICY SEGMENTS ---
{segments_text}
--- END SEGMENTS ---

Summary: {extraction_data.get('summary', 'N/A')}
"""

        print(f"\n⏳ Running Sentiment_Analyzer agent...")
        print(f"Analyzing {len(extraction_data.get('extracted_segments', []))} segments...")

        # Run sentiment analyzer agent
        result = await self.sentiment_analyzer.run(
            messages=prompt,
            temperature=0.0  # Deterministic output for consistency
        )

        # Extract text from result
        if hasattr(result, 'text'):
            response_text = result.text
        elif isinstance(result, str):
            response_text = result
        else:
            response_text = str(result)

        print(f"\n✓ Sentiment analysis completed")
        print(f"Response length: {len(response_text)} chars")

        # Try to parse JSON from response
        try:
            # Look for JSON in response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text

            sentiment_data = json.loads(json_text)
        except json.JSONDecodeError:
            print("⚠️  JSON parsing failed, using fallback structure")
            sentiment_data = {
                "overall_sentiment": "neutral",
                "sentiment_score": 0.0,
                "confidence": 0.0,
                "reasoning": "Could not parse sentiment results",
                "raw_response": response_text[:1000],
                "error": "JSON parsing failed"
            }

        # Add metadata
        sentiment_data['metadata'] = metadata
        sentiment_data['model'] = getattr(self.chat_client, 'model_id', 'unknown')

        return sentiment_data

    async def analyze_filing(
        self,
        item7_text: str,
        cik: str,
        year: str,
        save_results: bool = True
    ) -> Tuple[Dict, Dict]:
        """
        Run complete analysis pipeline on a single filing.

        Args:
            item7_text: Item 7 (MD&A) text
            cik: Company CIK
            year: Filing year
            save_results: Whether to save results to disk

        Returns:
            Tuple of (extraction_data, sentiment_data)

        Example:
            >>> pipeline = FinAgentPipeline()
            >>> extraction, sentiment = await pipeline.analyze_filing(
            ...     item7_text, "2186", "2020"
            ... )
            >>> print(f"Sentiment: {sentiment['overall_sentiment']}")
            >>> print(f"Score: {sentiment['sentiment_score']}")
        """
        metadata = {
            'cik': cik,
            'year': year,
            'word_count': len(item7_text.split()),
            'char_count': len(item7_text)
        }

        # Step 1: Extract policies
        extraction_data = await self.extract_policies(item7_text, metadata)

        # Step 2: Analyze sentiment
        sentiment_data = await self.analyze_sentiment(extraction_data, metadata)

        # Step 3: Save results if requested
        if save_results:
            print(f"\n💾 Saving results...")
            extraction_file = self.result_writer.save_extraction(cik, year, extraction_data)
            sentiment_file = self.result_writer.save_sentiment(cik, year, sentiment_data)
            print(f"✓ Extraction saved: {extraction_file}")
            print(f"✓ Sentiment saved: {sentiment_file}")

        return extraction_data, sentiment_data

    def print_summary(self, extraction_data: Dict, sentiment_data: Dict):
        """
        Print analysis summary.

        Args:
            extraction_data: Extraction results
            sentiment_data: Sentiment results
        """
        print(f"\n{'='*80}")
        print(f"ANALYSIS SUMMARY")
        print(f"{'='*80}")

        # Extraction summary
        segments = extraction_data.get('extracted_segments', [])
        print(f"\nExtraction Results:")
        print(f"  - Segments extracted: {len(segments)}")
        if segments:
            policy_types = [seg.get('policy_type', 'unknown') for seg in segments]
            print(f"  - Policy types: {', '.join(set(policy_types))}")
        print(f"  - Summary: {extraction_data.get('summary', 'N/A')}")

        # Sentiment summary
        print(f"\nSentiment Analysis:")
        print(f"  - Overall sentiment: {sentiment_data.get('overall_sentiment', 'N/A')}")
        print(f"  - Sentiment score: {sentiment_data.get('sentiment_score', 'N/A')}")
        print(f"  - Confidence: {sentiment_data.get('confidence', 'N/A')}")
        print(f"  - Reasoning: {sentiment_data.get('reasoning', 'N/A')}")

        print(f"\n{'='*80}\n")


# Convenience function
async def analyze_10k_filing(cik: str, year: str) -> Tuple[Dict, Dict]:
    """
    Convenience function to analyze a 10-K filing by CIK and year.

    Args:
        cik: Company CIK
        year: Filing year

    Returns:
        Tuple of (extraction_data, sentiment_data)

    Example:
        >>> extraction, sentiment = await analyze_10k_filing("2186", "2020")
        >>> print(f"Score: {sentiment['sentiment_score']}")
    """
    from finrobot.utils.data_loader import load_10k_item7

    # Load Item 7 text
    item7_text, metadata = load_10k_item7(cik, year)

    # Run pipeline
    pipeline = FinAgentPipeline()
    extraction, sentiment = await pipeline.analyze_filing(
        item7_text,
        cik,
        year,
        save_results=True
    )

    # Print summary
    pipeline.print_summary(extraction, sentiment)

    return extraction, sentiment
