#!/usr/bin/env python3
"""
Batch analysis script for 10-K filings.
Processes all available filings through the FinAgent pipeline.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from finrobot.workflows.finagent_pipeline import FinAgentPipeline
from finrobot.utils.data_loader import TenKDataLoader, ResultWriter


async def analyze_single_filing(
    pipeline: FinAgentPipeline,
    cik: str,
    year: str,
    item7_text: str
) -> Dict:
    """
    Analyze a single filing and return summary.

    Args:
        pipeline: FinAgent pipeline instance
        cik: Company CIK
        year: Filing year
        item7_text: Item 7 text

    Returns:
        Summary dictionary
    """
    print(f"\n{'#'*80}")
    print(f"# ANALYZING: {cik} ({year})")
    print(f"{'#'*80}\n")

    try:
        # Run analysis
        extraction, sentiment = await pipeline.analyze_filing(
            item7_text,
            cik,
            year,
            save_results=True
        )

        # Print summary
        pipeline.print_summary(extraction, sentiment)

        # Create summary record
        summary = {
            'cik': cik,
            'year': year,
            'success': True,
            'segments_extracted': len(extraction.get('extracted_segments', [])),
            'sentiment': sentiment.get('overall_sentiment', 'unknown'),
            'sentiment_score': sentiment.get('sentiment_score', 0.0),
            'confidence': sentiment.get('confidence', 0.0),
            'analysis_date': datetime.now().isoformat(),
            'error': None
        }

        return summary

    except Exception as e:
        print(f"\n✗ Error analyzing {cik} ({year}): {e}")
        import traceback
        traceback.print_exc()

        return {
            'cik': cik,
            'year': year,
            'success': False,
            'segments_extracted': 0,
            'sentiment': 'error',
            'sentiment_score': 0.0,
            'confidence': 0.0,
            'analysis_date': datetime.now().isoformat(),
            'error': str(e)
        }


async def batch_analyze(limit: int = None):
    """
    Batch analyze all available 10-K filings.

    Args:
        limit: Maximum number of filings to process (None = all)
    """
    print("\n" + "="*80)
    print("FINAGENT BATCH ANALYSIS")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize components
    loader = TenKDataLoader()
    pipeline = FinAgentPipeline()
    result_writer = ResultWriter()

    # Get available filings
    filings_info = loader.get_filing_info()
    total_filings = len(filings_info)

    if limit:
        filings_info = filings_info[:limit]

    print(f"Available filings: {total_filings}")
    print(f"Processing: {len(filings_info)}")
    print("\nFilings to process:")
    for info in filings_info:
        print(f"  - {info['cik']} ({info['year']}): {info['item7_words']:,} words")

    # Process each filing
    summaries = []

    for i, info in enumerate(filings_info, 1):
        print(f"\n\n{'='*80}")
        print(f"PROGRESS: {i}/{len(filings_info)}")
        print(f"{'='*80}")

        # Load Item 7 text
        filing = loader.load_filing_by_cik_year(info['cik'], info['year'])
        item7_text, metadata = loader.extract_item7(filing)

        # Analyze filing
        summary = await analyze_single_filing(
            pipeline,
            info['cik'],
            info['year'],
            item7_text
        )
        summaries.append(summary)

        # Progress update
        successful = sum(1 for s in summaries if s['success'])
        print(f"\n✓ Completed {i}/{len(filings_info)} ({successful} successful)")

    # Generate batch summary
    print(f"\n\n{'='*80}")
    print("BATCH ANALYSIS SUMMARY")
    print(f"{'='*80}\n")

    successful = [s for s in summaries if s['success']]
    failed = [s for s in summaries if not s['success']]

    print(f"Total processed: {len(summaries)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print(f"\nSentiment Distribution:")
        sentiments = {}
        for s in successful:
            sentiment = s['sentiment']
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1

        for sentiment, count in sorted(sentiments.items()):
            print(f"  - {sentiment.capitalize()}: {count}")

        avg_score = sum(s['sentiment_score'] for s in successful) / len(successful)
        avg_confidence = sum(s['confidence'] for s in successful) / len(successful)
        print(f"\nAverage sentiment score: {avg_score:.2f}")
        print(f"Average confidence: {avg_confidence:.2f}")

    if failed:
        print(f"\n⚠️  Failed filings:")
        for s in failed:
            print(f"  - {s['cik']} ({s['year']}): {s['error']}")

    # Save summary CSV
    print(f"\n💾 Saving batch summary...")

    # Prepare extraction summary
    extraction_summary = []
    for s in summaries:
        extraction_summary.append({
            'cik': s['cik'],
            'year': s['year'],
            'total_segments': s['segments_extracted'],
            'policy_types': '',  # Would need to extract from full results
            'extraction_date': s['analysis_date'],
            'success': s['success']
        })

    # Prepare sentiment summary
    sentiment_summary = []
    for s in summaries:
        sentiment_summary.append({
            'cik': s['cik'],
            'year': s['year'],
            'sentiment': s['sentiment'],
            'score': s['sentiment_score'],
            'confidence': s['confidence'],
            'analysis_date': s['analysis_date'],
            'success': s['success']
        })

    # Save summaries
    extraction_csv = result_writer.save_batch_summary(extraction_summary, 'extraction')
    sentiment_csv = result_writer.save_batch_summary(sentiment_summary, 'sentiment')

    print(f"✓ Extraction summary: {extraction_csv}")
    print(f"✓ Sentiment summary: {sentiment_csv}")

    print(f"\n{'='*80}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    return summaries


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Batch analyze 10-K filings using FinAgent pipeline'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Maximum number of filings to process (default: all)'
    )
    parser.add_argument(
        '--cik',
        type=str,
        help='Analyze only a specific CIK'
    )
    parser.add_argument(
        '--year',
        type=str,
        help='Analyze only a specific year (requires --cik)'
    )

    args = parser.parse_args()

    # Single filing mode
    if args.cik:
        if not args.year:
            print("Error: --year is required when using --cik")
            sys.exit(1)

        from finrobot.workflows.finagent_pipeline import analyze_10k_filing
        await analyze_10k_filing(args.cik, args.year)
        return 0

    # Batch mode
    await batch_analyze(limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
