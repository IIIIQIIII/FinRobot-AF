"""
Test FLS Detection Toolkit
===========================

Simple test script to verify FLS detection functionality without LLM calls.
Uses rule-based signal word detection.

Usage:
    python examples/test_fls_detection.py
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from finrobot.functional.fls_detection import (
    detect_fls_signal_words,
    calculate_fls_score,
    extract_sentences_with_signals,
    analyze_fls_in_text,
    classify_fls_category_mda,
    classify_fls_category_risk
)


def test_signal_detection():
    """Test basic FLS signal word detection."""
    print("="*60)
    print("TEST 1: Signal Word Detection")
    print("="*60)

    test_texts = [
        "We expect revenue to grow 5-7% in the next fiscal year.",
        "The company plans to expand operations in Asia-Pacific markets.",
        "Revenue increased 8% in Q4 2020.",  # Historical, not FLS
        "We believe the new product will capture significant market share.",
        "Interest rates may increase, adversely affecting our borrowing costs."
    ]

    for i, text in enumerate(test_texts, 1):
        signals = detect_fls_signal_words(text)
        score = calculate_fls_score(text)

        print(f"\n[{i}] {text}")
        print(f"    Signals: {signals}")
        print(f"    FLS Score: {score:.3f}")
        print(f"    Likely FLS: {'✓' if score > 0.3 else '✗'}")


def test_sentence_extraction():
    """Test sentence-level FLS extraction."""
    print("\n" + "="*60)
    print("TEST 2: Sentence Extraction with Context")
    print("="*60)

    text = """
    In 2020, revenue increased 12% to $5.2 billion. We expect continued growth
    in the coming year, driven by new product launches. The company plans to
    invest $500M in R&D over the next three years. Competition remains intense
    in our core markets.
    """

    sentences = extract_sentences_with_signals(text, min_signals=1, context_sentences=0)

    print(f"\nInput text: {text.strip()}")
    print(f"\nFound {len(sentences)} sentences with FLS signals:\n")

    for sent in sentences:
        print(f"  [{sent['sentence_id']}] {sent['text']}")
        print(f"      Signals: {sent['signal_words']}")
        print(f"      Score: {sent['fls_score']:.3f}\n")


def test_full_analysis():
    """Test complete FLS analysis on sample text."""
    print("="*60)
    print("TEST 3: Full FLS Analysis")
    print("="*60)

    sample_mda = """
    Management's Discussion and Analysis

    Results of Operations:
    Revenue for fiscal 2020 was $10.5 billion, an increase of 8% from the prior year.
    Net income was $1.2 billion, up 12% year-over-year.

    Outlook and Future Plans:
    Looking ahead, we expect revenue growth of 6-8% in fiscal 2021, driven by strong
    demand for our cloud services. We plan to expand our data center capacity with
    investments of approximately $800 million. Management believes these investments
    will position us well for long-term growth.

    The company intends to return capital to shareholders through our dividend program,
    which we expect to increase by 10% annually. We may also opportunistically repurchase
    shares when market conditions are favorable.

    Risks and Uncertainties:
    Our business could be adversely affected by changes in foreign exchange rates,
    which might reduce our reported earnings. Increased competition may pressure
    our pricing and margins.
    """

    analysis = analyze_fls_in_text(sample_mda, "Sample MD&A", min_confidence=0.3)

    print(f"\nSection: {analysis['section']}")
    print(f"Total FLS found: {analysis['total_fls_found']}")
    print(f"Average FLS score: {analysis['average_fls_score']:.3f}")
    print(f"Signal categories: {list(analysis['signal_categories'].keys())}")
    print(f"\nMetadata:")
    print(f"  Text length: {analysis['metadata']['text_length']:,} chars")
    print(f"  Total sentences: {analysis['metadata']['total_sentences']}")
    print(f"  FLS density: {analysis['metadata']['fls_density']:.3f}")

    print(f"\nTop FLS segments:")
    for i, segment in enumerate(analysis['fls_segments'][:5], 1):
        print(f"\n  [{i}] {segment['text'][:100]}...")
        print(f"      Score: {segment['fls_score']:.3f}")
        print(f"      Signals: {segment['signal_words']}")


def test_categorization():
    """Test FLS categorization."""
    print("\n" + "="*60)
    print("TEST 4: FLS Categorization")
    print("="*60)

    mda_examples = [
        "We expect revenue to grow 8% next year.",
        "The company plans to expand into Asian markets.",
        "We intend to increase our dividend by 15%.",
        "Management believes market demand will remain strong.",
    ]

    risk_examples = [
        "Increased competition could reduce our market share.",
        "Regulatory changes may require significant compliance costs.",
        "Supply chain disruptions could affect operations.",
        "Rising interest rates would increase our debt costs.",
    ]

    print("\nMD&A FLS Categories:")
    for text in mda_examples:
        category = classify_fls_category_mda(text)
        print(f"  {category:20s} - {text}")

    print("\nRisk Factor FLS Categories:")
    for text in risk_examples:
        category = classify_fls_category_risk(text)
        print(f"  {category:20s} - {text}")


def test_real_filing():
    """Test on actual 10-K filing data."""
    print("\n" + "="*60)
    print("TEST 5: Real 10-K Filing Analysis")
    print("="*60)

    # Load Abbott 2020 filing
    filing_path = Path(__file__).parent.parent / "data/10k_filings/1800_2020.json"

    if not filing_path.exists():
        print(f"  ⚠ Skipping - filing not found: {filing_path}")
        return

    with open(filing_path) as f:
        data = json.load(f)

    section_7 = data.get('section_7', '')
    section_1a = data.get('section_1A', '')

    print(f"\nFiling: Abbott Laboratories (CIK: 1800, Year: 2020)")
    print(f"Section 7 length: {len(section_7):,} characters")
    print(f"Section 1A length: {len(section_1a):,} characters")

    # Analyze Section 7 (sample - first 20k chars for speed)
    print("\n--- Section 7 (MD&A) Analysis ---")
    mda_sample = section_7[:20000]
    mda_analysis = analyze_fls_in_text(mda_sample, "Section 7 - MD&A", min_confidence=0.4)

    print(f"FLS found: {mda_analysis['total_fls_found']}")
    print(f"Avg confidence: {mda_analysis['average_fls_score']:.3f}")
    print(f"Signal categories: {list(mda_analysis['signal_categories'].keys())}")

    # Show sample FLS
    if mda_analysis['fls_segments']:
        print(f"\nSample FLS from MD&A:")
        for i, seg in enumerate(mda_analysis['fls_segments'][:3], 1):
            print(f"\n  [{i}] {seg['text'][:150]}...")
            print(f"      Score: {seg['fls_score']:.3f}")

    # Analyze Section 1A (sample)
    print("\n--- Section 1A (Risk Factors) Analysis ---")
    risk_sample = section_1a[:20000]
    risk_analysis = analyze_fls_in_text(risk_sample, "Section 1A - Risk Factors", min_confidence=0.4)

    print(f"FLS found: {risk_analysis['total_fls_found']}")
    print(f"Avg confidence: {risk_analysis['average_fls_score']:.3f}")
    print(f"Signal categories: {list(risk_analysis['signal_categories'].keys())}")

    # Show sample FLS
    if risk_analysis['fls_segments']:
        print(f"\nSample FLS from Risk Factors:")
        for i, seg in enumerate(risk_analysis['fls_segments'][:3], 1):
            print(f"\n  [{i}] {seg['text'][:150]}...")
            print(f"      Score: {seg['fls_score']:.3f}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FLS DETECTION TOOLKIT TEST SUITE")
    print("="*60)

    test_signal_detection()
    test_sentence_extraction()
    test_full_analysis()
    test_categorization()
    test_real_filing()

    print("\n" + "="*60)
    print("✓ All tests completed!")
    print("="*60 + "\n")
