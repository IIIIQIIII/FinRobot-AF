"""
End-to-end test for FinAgent pipeline.
Tests policy extraction and sentiment analysis on real 10-K data.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


async def test_single_filing_analysis():
    """Test analyzing a single 10-K filing."""
    print("\n" + "="*80)
    print("TEST: Single Filing Analysis")
    print("="*80)

    try:
        from finrobot.workflows.finagent_pipeline import analyze_10k_filing

        # Analyze CIK 2186, year 2020
        print("\n⏳ Analyzing 10-K filing: CIK 2186 (2020)...")

        extraction, sentiment = await analyze_10k_filing("2186", "2020")

        # Validate results
        assert 'extracted_segments' in extraction, "Missing 'extracted_segments' in extraction"
        assert 'overall_sentiment' in sentiment, "Missing 'overall_sentiment' in sentiment"
        assert 'sentiment_score' in sentiment, "Missing 'sentiment_score' in sentiment"

        print(f"\n✅ Single filing analysis test passed!")
        print(f"   - Segments extracted: {len(extraction.get('extracted_segments', []))}")
        print(f"   - Overall sentiment: {sentiment.get('overall_sentiment', 'N/A')}")
        print(f"   - Sentiment score: {sentiment.get('sentiment_score', 'N/A')}")

        return True

    except Exception as e:
        print(f"\n✗ Single filing analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_data_loader():
    """Test 10-K data loader utilities."""
    print("\n" + "="*80)
    print("TEST: Data Loader")
    print("="*80)

    try:
        from finrobot.utils.data_loader import (
            TenKDataLoader,
            list_available_filings,
            load_10k_item7
        )

        # Test listing files
        print("\n⏳ Testing file listing...")
        loader = TenKDataLoader()
        files = loader.list_files()
        print(f"✓ Found {len(files)} 10-K files")

        assert len(files) >= 5, "Should have at least 5 files"

        # Test filing info
        print("\n⏳ Testing filing info...")
        info = list_available_filings()
        print(f"✓ Retrieved info for {len(info)} filings")

        for filing in info:
            print(f"   - {filing['cik']} ({filing['year']}): {filing['item7_words']:,} words")

        # Test loading Item 7
        print("\n⏳ Testing Item 7 loading...")
        item7_text, metadata = load_10k_item7("2186", "2020")
        print(f"✓ Loaded Item 7:")
        print(f"   - CIK: {metadata['cik']}")
        print(f"   - Year: {metadata['year']}")
        print(f"   - Words: {metadata['word_count']:,}")
        print(f"   - Chars: {metadata['char_count']:,}")

        assert len(item7_text) > 1000, "Item 7 text should be substantial"
        assert metadata['word_count'] > 100, "Should have meaningful word count"

        print(f"\n✅ Data loader test passed!")
        return True

    except Exception as e:
        print(f"\n✗ Data loader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_configs():
    """Test that Policy_Extractor and Sentiment_Analyzer agents are configured."""
    print("\n" + "="*80)
    print("TEST: Agent Configurations")
    print("="*80)

    try:
        from finrobot.agents.agent_library import AGENT_CONFIGS

        # Check Policy_Extractor
        print("\n⏳ Checking Policy_Extractor configuration...")
        assert "Policy_Extractor" in AGENT_CONFIGS, "Policy_Extractor not found in agent library"
        extractor_config = AGENT_CONFIGS["Policy_Extractor"]
        assert "instructions" in extractor_config, "Missing instructions"
        assert "macroeconomic policy" in extractor_config["instructions"].lower(), \
            "Instructions should mention macroeconomic policy"
        print(f"✓ Policy_Extractor configured")

        # Check Sentiment_Analyzer
        print("\n⏳ Checking Sentiment_Analyzer configuration...")
        assert "Sentiment_Analyzer" in AGENT_CONFIGS, "Sentiment_Analyzer not found in agent library"
        analyzer_config = AGENT_CONFIGS["Sentiment_Analyzer"]
        assert "instructions" in analyzer_config, "Missing instructions"
        assert "sentiment" in analyzer_config["instructions"].lower(), \
            "Instructions should mention sentiment"
        print(f"✓ Sentiment_Analyzer configured")

        print(f"\n✅ Agent configuration test passed!")
        return True

    except Exception as e:
        print(f"\n✗ Agent configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_pipeline_creation():
    """Test creating FinAgent pipeline without running full analysis."""
    print("\n" + "="*80)
    print("TEST: Pipeline Creation")
    print("="*80)

    try:
        from finrobot.workflows.finagent_pipeline import FinAgentPipeline
        from finrobot.config import FinRobotConfig

        print("\n⏳ Creating FinAgent pipeline...")
        config = FinRobotConfig()
        pipeline = FinAgentPipeline(config)

        assert pipeline.extractor is not None, "Extractor agent not created"
        assert pipeline.sentiment_analyzer is not None, "Sentiment analyzer not created"
        assert pipeline.chat_client is not None, "Chat client not initialized"

        print(f"✓ Pipeline created successfully")
        print(f"   - Extractor: {pipeline.extractor.name}")
        print(f"   - Sentiment Analyzer: {pipeline.sentiment_analyzer.name}")
        print(f"   - Chat Client: {type(pipeline.chat_client).__name__}")

        print(f"\n✅ Pipeline creation test passed!")
        return True

    except Exception as e:
        print(f"\n✗ Pipeline creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all FinAgent tests."""
    print("\n" + "="*80)
    print("FINAGENT PIPELINE TEST SUITE")
    print("="*80)
    print(f"Testing policy extraction and sentiment analysis system\n")

    results = []

    # Test 1: Data loader
    results.append(("Data Loader", await test_data_loader()))

    # Test 2: Agent configurations
    results.append(("Agent Configurations", await test_agent_configs()))

    # Test 3: Pipeline creation
    results.append(("Pipeline Creation", await test_pipeline_creation()))

    # Test 4: Single filing analysis (full E2E)
    # Only run if previous tests passed
    if all(r for _, r in results):
        results.append(("Single Filing Analysis", await test_single_filing_analysis()))
    else:
        print("\n⚠️  Skipping full analysis test due to previous failures")
        results.append(("Single Filing Analysis", False))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, p in results if p)
    total = len(results)

    print(f"\nResults: {passed}/{total} tests passed")
    print("="*80 + "\n")

    if passed == total:
        print("🎉 All FinAgent tests passed!")
        print("✅ FinAgent pipeline is ready for production use!\n")
        return 0
    else:
        print("⚠️  Some tests failed. Please review errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
