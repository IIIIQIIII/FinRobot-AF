"""
Test Sentiment Analysis with Aliyun Qwen3-Max
=============================================

Test FinRobot-AF sentiment analysis using Aliyun DashScope (Qwen models).
Results are saved to results/ directory.
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from finrobot.workflows.finagent_pipeline import FinAgentPipeline
from finrobot.config import FinRobotConfig
from finrobot.llm_config import switch_provider


def load_10k_item7(cik: str, year: str):
    """Load 10-K Item 7 text from JSON file."""
    data_dir = Path(__file__).parent.parent / "data" / "10k_filings"
    file_path = data_dir / f"{cik}_{year}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Filing not found: {file_path}")

    with open(file_path) as f:
        data = json.load(f)

    # Try different keys for Item 7
    item7_text = data.get('item7_mda') or data.get('section_7') or data.get('item_7', '')

    if not item7_text:
        raise ValueError(f"No Item 7 found in {file_path}")

    metadata = {
        'cik': cik,
        'year': year,
        'word_count': len(item7_text.split()),
        'char_count': len(item7_text)
    }

    return item7_text, metadata


async def test_sentiment_analysis():
    """Test sentiment analysis with Qwen."""

    print("="*80)
    print("Sentiment Analysis Test - Aliyun Qwen3-Max")
    print("="*80)
    print()

    # Switch to Aliyun Qwen3-Max
    print("Step 1: Configure LLM Provider")
    print("-" * 80)
    switch_provider("aliyun", "qwen3-max")
    print()

    # Initialize FinRobot
    print("Step 2: Initialize FinRobot-AF")
    print("-" * 80)
    config = FinRobotConfig()
    pipeline = FinAgentPipeline(config)
    print("✓ FinAgent pipeline initialized")
    print()

    # Test on Abbott Laboratories
    print("Step 3: Load Test Data")
    print("-" * 80)
    cik = "1800"
    year = "2020"
    print(f"Company: Abbott Laboratories (CIK: {cik})")
    print(f"Year: {year}")

    item7_text, metadata = load_10k_item7(cik, year)
    print(f"Item 7 length: {metadata['word_count']:,} words")
    print()

    # Extract policies
    print("Step 4: Extract Policy Segments")
    print("-" * 80)
    extraction_result = await pipeline.extract_policies(item7_text, metadata)

    segments = extraction_result.get('extracted_segments', [])
    print(f"✓ Extracted {len(segments)} policy segments")

    # Show first 3 segments
    print("\nSample segments:")
    for i, seg in enumerate(segments[:3], 1):
        print(f"\n  Segment {i}:")
        print(f"    Type: {seg.get('policy_type', 'N/A')}")
        print(f"    Text: {seg.get('text', '')[:100]}...")
    print()

    # Analyze sentiment
    print("Step 5: Analyze Sentiment")
    print("-" * 80)
    sentiment_result = await pipeline.analyze_sentiment(extraction_result, metadata)

    print(f"Overall Sentiment: {sentiment_result.get('overall_sentiment', 'N/A')}")
    print(f"Sentiment Score: {sentiment_result.get('sentiment_score', 0):+.2f}")
    print(f"Confidence: {sentiment_result.get('confidence', 0):.2f}")

    reasoning = sentiment_result.get('reasoning', '')
    print(f"\nReasoning:")
    print(f"  {reasoning[:200]}...")
    print()

    # Segment-level sentiment
    seg_sentiments = sentiment_result.get('segment_sentiments', [])
    if seg_sentiments:
        print(f"Segment-level sentiments: {len(seg_sentiments)} segments")

        # Count by sentiment
        sentiment_counts = {}
        for seg_sent in seg_sentiments:
            sent = seg_sent.get('sentiment', 'unknown')
            sentiment_counts[sent] = sentiment_counts.get(sent, 0) + 1

        print("  Distribution:")
        for sent, count in sorted(sentiment_counts.items()):
            pct = count / len(seg_sentiments) * 100
            print(f"    {sent}: {count} ({pct:.1f}%)")
    print()

    # Save results
    print("Step 6: Save Results")
    print("-" * 80)

    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    output_data = {
        "metadata": {
            "cik": cik,
            "year": year,
            "company": "Abbott Laboratories",
            "llm_provider": "aliyun",
            "llm_model": "qwen3-max",
            "timestamp": datetime.now().isoformat()
        },
        "extraction": {
            "segments_count": len(segments),
            "segments": segments,
            "summary": extraction_result.get('summary', '')
        },
        "sentiment": {
            "overall_sentiment": sentiment_result.get('overall_sentiment'),
            "sentiment_score": sentiment_result.get('sentiment_score'),
            "confidence": sentiment_result.get('confidence'),
            "reasoning": sentiment_result.get('reasoning'),
            "segment_sentiments": seg_sentiments
        }
    }

    # Save to results
    output_file = results_dir / f"sentiment_qwen_{cik}_{year}.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"✓ Results saved to: {output_file}")
    print()

    # Summary
    print("="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    print(f"LLM Provider: Aliyun DashScope (Qwen3-Max)")
    print(f"Company: Abbott Laboratories ({cik})")
    print(f"Year: {year}")
    print()
    print(f"Extraction:")
    print(f"  Segments: {len(segments)}")
    print()
    print(f"Sentiment:")
    print(f"  Overall: {sentiment_result.get('overall_sentiment', 'N/A')}")
    print(f"  Score: {sentiment_result.get('sentiment_score', 0):+.2f}")
    print(f"  Confidence: {sentiment_result.get('confidence', 0):.2f}")
    print()
    print(f"Output File:")
    print(f"  {output_file}")
    print()
    print("✅ Test completed successfully!")
    print()


if __name__ == "__main__":
    asyncio.run(test_sentiment_analysis())
