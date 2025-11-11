"""
Batch FLS Extraction Script
============================

Run FLS extraction on all available 10-K filings in data/10k_filings/
"""

import sys
import asyncio
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.fls_extraction_10k import FLSExtractionWorkflow


async def main():
    # Get all 10-K filings (go up to project root)
    project_root = Path(__file__).parent.parent
    data_folder = project_root / "data/10k_filings"
    filings = sorted(data_folder.glob("*.json"))

    print("="*60)
    print("BATCH FLS EXTRACTION")
    print("="*60)
    print(f"Found {len(filings)} 10-K filings")
    print()

    # Initialize workflow
    workflow = FLSExtractionWorkflow("fls_extraction")

    results_summary = []

    for filing_path in filings:
        # Extract CIK and year from filename (format: CIK_YEAR.json)
        filename = filing_path.stem  # e.g., "1800_2020"
        try:
            cik, year = filename.split('_')
        except ValueError:
            print(f"⚠ Skipping {filename} - invalid format")
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print(f"{'='*60}")

        try:
            # Run FLS extraction
            output_file = await workflow.analyze_filing(cik, year)

            # Load results for summary
            with open(output_file) as f:
                result_data = json.load(f)

            summary = {
                'cik': cik,
                'year': year,
                'filename': filename,
                'mda_fls': result_data['section_7_mda']['fls_count'],
                'risk_fls': result_data['section_1a_risks']['fls_count'],
                'total_fls': result_data['combined_statistics']['total_fls_extracted'],
                'output_file': str(output_file)
            }

            results_summary.append(summary)

            print(f"\n✓ Completed: {filename}")
            print(f"  MD&A FLS: {summary['mda_fls']}")
            print(f"  Risk FLS: {summary['risk_fls']}")
            print(f"  Total: {summary['total_fls']}")

        except Exception as e:
            print(f"\n✗ Failed: {filename}")
            print(f"  Error: {str(e)}")
            results_summary.append({
                'cik': cik,
                'year': year,
                'filename': filename,
                'error': str(e)
            })

    # Print final summary
    print(f"\n\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total filings processed: {len(results_summary)}")
    print()

    # Success summary
    successful = [r for r in results_summary if 'total_fls' in r]
    failed = [r for r in results_summary if 'error' in r]

    if successful:
        print(f"✓ Successful: {len(successful)}")
        print("\nResults:")
        print(f"{'Filename':<20} {'MD&A FLS':>10} {'Risk FLS':>10} {'Total':>10}")
        print("-" * 60)
        for r in successful:
            print(f"{r['filename']:<20} {r['mda_fls']:>10} {r['risk_fls']:>10} {r['total_fls']:>10}")

    if failed:
        print(f"\n✗ Failed: {len(failed)}")
        for r in failed:
            print(f"  {r['filename']}: {r['error']}")

    # Save batch summary
    summary_file = project_root / "results/fls_extraction/batch_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'total_processed': len(results_summary),
            'successful': len(successful),
            'failed': len(failed),
            'results': results_summary
        }, f, indent=2)

    print(f"\n✓ Batch summary saved to: {summary_file}")


if __name__ == "__main__":
    asyncio.run(main())
