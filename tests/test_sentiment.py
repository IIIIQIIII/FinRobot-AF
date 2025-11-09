#!/usr/bin/env python
"""
Test script for sentiment analysis functionality.
Tests the FinAgent pipeline with sample text.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_sentiment_analysis():
    """Test sentiment analysis with sample text."""

    print("="*80)
    print("FinRobot Sentiment Analysis Test")
    print("="*80)
    print()

    # Step 1: Import and check dependencies
    print("Step 1: Checking imports...")
    try:
        from finrobot.workflows.finagent_pipeline import FinAgentPipeline
        from finrobot.config import FinRobotConfig
        print("✅ Successfully imported FinAgent pipeline modules")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

    # Step 2: Check if config files exist
    print("\nStep 2: Checking configuration...")
    config_files = {
        'OAI_CONFIG_LIST': Path('OAI_CONFIG_LIST'),
        'config_api_keys': Path('config_api_keys'),
    }

    missing_configs = []
    for name, path in config_files.items():
        if path.exists():
            print(f"✅ Found {name}")
        else:
            print(f"⚠️  Missing {name} (will use environment variables)")
            missing_configs.append(name)

    # Step 3: Initialize pipeline
    print("\nStep 3: Initializing FinAgent pipeline...")
    try:
        # Try to initialize with config
        config = FinRobotConfig()
        pipeline = FinAgentPipeline(config)
        print("✅ Pipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        print("\nPlease ensure you have:")
        print("  1. Created OAI_CONFIG_LIST with your OpenAI API key")
        print("  2. Or set OPENAI_API_KEY environment variable")
        return False

    # Step 4: Test with sample text
    print("\nStep 4: Testing sentiment analysis with sample text...")

    sample_text = """
    The Federal Reserve's recent interest rate policies have created
    significant uncertainty in the market. While some analysts view
    the tightening as necessary to combat inflation, others express
    concern about potential recession risks. Our company remains
    cautiously optimistic about navigating these challenges, though
    we acknowledge the headwinds facing the broader economy.
    """

    # Create sample extraction data (simulating policy extractor output)
    extraction_data = {
        'extracted_segments': [
            {
                'segment_id': 1,
                'text': sample_text.strip(),
                'policy_type': 'monetary_policy'
            }
        ],
        'total_segments': 1
    }

    metadata = {
        'cik': 'TEST-CIK',
        'year': '2024',
        'company_name': 'Test Company'
    }

    try:
        print("\nAnalyzing sentiment...")
        print(f"Sample text: {sample_text[:100]}...")

        sentiment_result = await pipeline.analyze_sentiment(
            extraction_data,
            metadata
        )

        print("\n" + "="*80)
        print("SENTIMENT ANALYSIS RESULTS")
        print("="*80)
        print(f"Overall Sentiment: {sentiment_result.get('overall_sentiment', 'N/A')}")
        print(f"Sentiment Score: {sentiment_result.get('sentiment_score', 'N/A')}")
        print(f"Confidence: {sentiment_result.get('confidence', 'N/A')}")
        print(f"Reasoning: {sentiment_result.get('reasoning', 'N/A')}")
        print("="*80)

        print("\n✅ Sentiment analysis completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Sentiment analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_basic_imports():
    """Test basic imports without API calls."""
    print("="*80)
    print("FinRobot Basic Import Test")
    print("="*80)
    print()

    tests = [
        ('finrobot', 'Core package'),
        ('finrobot.config', 'Configuration module'),
        ('finrobot.workflows.finagent_pipeline', 'FinAgent pipeline'),
        ('finrobot.agents.agent_library', 'Agent library'),
        ('finrobot.utils.data_loader', 'Data loader utilities'),
    ]

    all_passed = True
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✅ {description:.<50} OK")
        except ImportError as e:
            print(f"❌ {description:.<50} FAILED: {e}")
            all_passed = False

    print()
    return all_passed


def main():
    """Main test runner."""
    import argparse

    parser = argparse.ArgumentParser(description='Test FinRobot sentiment analysis')
    parser.add_argument(
        '--import-only',
        action='store_true',
        help='Only test imports, skip API calls'
    )
    args = parser.parse_args()

    if args.import_only:
        result = asyncio.run(test_basic_imports())
    else:
        result = asyncio.run(test_sentiment_analysis())

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
