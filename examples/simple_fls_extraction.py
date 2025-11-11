"""
Simple FLS Extraction Example
==============================

Extract Forward-Looking Statements from 10-K filings using the FLS detection toolkit.
This example uses rule-based detection without LLM for fast batch processing.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from finrobot.functional.fls_detection import analyze_fls_in_text


def extract_fls_from_filing(cik: str, year: str, output_folder: Path):
    """
    Extract FLS from a 10-K filing using rule-based detection.

    Args:
        cik: Company CIK
        year: Filing year
        output_folder: Where to save results
    """
    # Load filing
    filing_path = Path(__file__).parent.parent / f"data/10k_filings/{cik}_{year}.json"

    if not filing_path.exists():
        raise FileNotFoundError(f"Filing not found: {filing_path}")

    with open(filing_path) as f:
        data = json.load(f)

    # Extract sections
    section_7 = data.get('section_7', '')
    section_1a = data.get('section_1A', '')

    print(f"\n{'='*60}")
    print(f"FLS EXTRACTION: {cik} ({year})")
    print(f"{'='*60}")
    print(f"Section 7 length: {len(section_7):,} chars")
    print(f"Section 1A length: {len(section_1a):,} chars")

    # Analyze Section 7 (MD&A)
    print(f"\nAnalyzing Section 7 (MD&A)...")
    mda_analysis = analyze_fls_in_text(
        section_7,
        section_name="Section 7 - MD&A",
        min_confidence=0.5
    )
    print(f"  Found {mda_analysis['total_fls_found']} FLS segments")
    print(f"  Avg confidence: {mda_analysis['average_fls_score']:.3f}")

    # Analyze Section 1A (Risk Factors)
    print(f"\nAnalyzing Section 1A (Risk Factors)...")
    risk_analysis = analyze_fls_in_text(
        section_1a,
        section_name="Section 1A - Risk Factors",
        min_confidence=0.5
    )
    print(f"  Found {risk_analysis['total_fls_found']} FLS segments")
    print(f"  Avg confidence: {risk_analysis['average_fls_score']:.3f}")

    # Combine results
    combined_results = {
        "metadata": {
            "cik": cik,
            "year": year,
            "filename": f"{cik}_{year}",
            "extraction_timestamp": datetime.now().isoformat(),
            "method": "rule_based_toolkit"
        },
        "section_7_mda": {
            "fls_count": mda_analysis['total_fls_found'],
            "average_confidence": mda_analysis['average_fls_score'],
            "signal_categories": mda_analysis['signal_categories'],
            "fls_segments": mda_analysis['fls_segments'][:20],  # Top 20
            "metadata": mda_analysis['metadata']
        },
        "section_1a_risks": {
            "fls_count": risk_analysis['total_fls_found'],
            "average_confidence": risk_analysis['average_fls_score'],
            "signal_categories": risk_analysis['signal_categories'],
            "fls_segments": risk_analysis['fls_segments'][:20],  # Top 20
            "metadata": risk_analysis['metadata']
        },
        "combined_statistics": {
            "total_fls_extracted": mda_analysis['total_fls_found'] + risk_analysis['total_fls_found'],
            "mda_fls": mda_analysis['total_fls_found'],
            "risk_fls": risk_analysis['total_fls_found']
        }
    }

    # Save results
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"fls_{cik}_{year}.json"

    with open(output_file, 'w') as f:
        json.dump(combined_results, f, indent=2)

    print(f"\n✓ Results saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  Section 7: {combined_results['section_7_mda']['fls_count']} FLS")
    print(f"  Section 1A: {combined_results['section_1a_risks']['fls_count']} FLS")
    print(f"  Total: {combined_results['combined_statistics']['total_fls_extracted']} FLS")

    return output_file


def main():
    """Run FLS extraction on all available filings."""
    # Get all 10-K filings
    data_folder = Path(__file__).parent.parent / "data/10k_filings"
    filings = sorted(data_folder.glob("*.json"))

    output_folder = Path(__file__).parent.parent / "results/fls_extraction"

    print("="*60)
    print("SIMPLE FLS EXTRACTION (Rule-Based)")
    print("="*60)
    print(f"Found {len(filings)} 10-K filings\n")

    results_summary = []

    for filing_path in filings:
        filename = filing_path.stem
        try:
            cik, year = filename.split('_')
        except ValueError:
            print(f"⚠ Skipping {filename} - invalid format")
            continue

        try:
            output_file = extract_fls_from_filing(cik, year, output_folder)

            # Load for summary
            with open(output_file) as f:
                result_data = json.load(f)

            results_summary.append({
                'cik': cik,
                'year': year,
                'filename': filename,
                'mda_fls': result_data['section_7_mda']['fls_count'],
                'risk_fls': result_data['section_1a_risks']['fls_count'],
                'total_fls': result_data['combined_statistics']['total_fls_extracted']
            })

        except Exception as e:
            print(f"\n✗ Failed: {filename} - {str(e)}")
            results_summary.append({
                'cik': cik,
                'year': year,
                'filename': filename,
                'error': str(e)
            })

    # Print summary
    print(f"\n\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total filings processed: {len(results_summary)}\n")

    successful = [r for r in results_summary if 'total_fls' in r]
    failed = [r for r in results_summary if 'error' in r]

    if successful:
        print(f"✓ Successful: {len(successful)}\n")
        print(f"{'Filename':<20} {'MD&A FLS':>10} {'Risk FLS':>10} {'Total':>10}")
        print("-" * 60)
        for r in successful:
            print(f"{r['filename']:<20} {r['mda_fls']:>10} {r['risk_fls']:>10} {r['total_fls']:>10}")

    if failed:
        print(f"\n✗ Failed: {len(failed)}")
        for r in failed:
            print(f"  {r['filename']}: {r['error']}")

    # Save batch summary
    summary_file = output_folder / "simple_batch_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'total_processed': len(results_summary),
            'successful': len(successful),
            'failed': len(failed),
            'results': results_summary
        }, f, indent=2)

    print(f"\n✓ Batch summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
