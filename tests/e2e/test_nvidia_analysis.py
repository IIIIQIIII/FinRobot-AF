"""
Real-World Test: NVIDIA Stock Analysis

This script demonstrates FinRobot-AF's capabilities by performing
a comprehensive analysis of NVIDIA (NVDA) stock using real financial data.
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path


async def test_market_analyst_nvda():
    """Test Market_Analyst with NVIDIA stock."""
    print("=" * 80)
    print("REAL-WORLD TEST: NVIDIA Stock Analysis with Market_Analyst")
    print("=" * 80)

    # Prepare report storage
    all_results = []

    try:
        from finrobot.agents.workflows import SingleAssistant
        from finrobot.agents.response_utils import extract_response_text

        print("\n🤖 Creating Market_Analyst...")
        analyst = SingleAssistant("Market_Analyst")
        print("✓ Market_Analyst created with financial data tools\n")

        # Test 1: Company Profile
        print("=" * 80)
        print("Test 1: Get NVIDIA Company Profile")
        print("=" * 80)

        query1 = "Get the company profile for NVIDIA (NVDA). Summarize the key information."
        print(f"\n📊 Query: {query1}\n")

        response1 = await analyst.chat(query1)
        result1 = extract_response_text(response1)

        print("✓ Response received:")
        print("-" * 80)
        print(result1)
        print("-" * 80)

        all_results.append(("Company Profile", result1))

        # Test 2: Recent News
        print("\n" + "=" * 80)
        print("Test 2: Get Recent NVIDIA News")
        print("=" * 80)

        query2 = "Get the latest news about NVIDIA (NVDA). Summarize the top 3 most important stories."
        print(f"\n📰 Query: {query2}\n")

        response2 = await analyst.chat(query2)
        result2 = extract_response_text(response2)

        print("✓ Response received:")
        print("-" * 80)
        print(result2)
        print("-" * 80)

        all_results.append(("Recent News", result2))

        # Test 3: Stock Data
        print("\n" + "=" * 80)
        print("Test 3: Get NVIDIA Stock Price Data")
        print("=" * 80)

        query3 = "Get NVIDIA (NVDA) stock price data for the last 30 days. What's the current trend?"
        print(f"\n📈 Query: {query3}\n")

        response3 = await analyst.chat(query3)
        result3 = extract_response_text(response3)

        print("✓ Response received:")
        print("-" * 80)
        print(result3)
        print("-" * 80)

        all_results.append(("Stock Price Data", result3))

        # Test 4: Financial Metrics
        print("\n" + "=" * 80)
        print("Test 4: Get NVIDIA Financial Metrics")
        print("=" * 80)

        query4 = "Get NVIDIA's basic financial metrics. What are the key ratios?"
        print(f"\n💰 Query: {query4}\n")

        response4 = await analyst.chat(query4)
        result4 = extract_response_text(response4)

        print("✓ Response received:")
        print("-" * 80)
        print(result4)
        print("-" * 80)

        all_results.append(("Financial Metrics", result4))

        print("\n✅ Market_Analyst NVIDIA analysis complete!\n")
        return True, all_results

    except Exception as e:
        print(f"\n✗ Market_Analyst test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, all_results


async def test_multi_agent_nvda_analysis():
    """Test multi-agent collaboration on NVIDIA analysis."""
    print("\n" + "=" * 80)
    print("MULTI-AGENT TEST: Comprehensive NVIDIA Analysis")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistant
        from finrobot.agents.response_utils import extract_response_text

        print("\n🤖 Creating multi-agent team...")
        team = MultiAssistant([
            "Market_Analyst",
            "Financial_Analyst",
            "Statistician"
        ])

        print("✓ Team created:")
        for agent in team.agents:
            print(f"  - {agent.name}")

        task = """
        Perform a comprehensive analysis of NVIDIA (NVDA) stock:

        Market_Analyst:
        - Get current stock price and recent performance
        - Identify key market trends affecting NVIDIA

        Financial_Analyst:
        - Analyze NVIDIA's financial health
        - Assess valuation metrics

        Statistician:
        - Evaluate stock volatility
        - Assess risk factors

        Provide a unified investment recommendation based on all perspectives.
        Keep each section concise (2-3 sentences).
        """

        print(f"\n📊 Collaborative Analysis Task:")
        print(task)
        print("\n🔄 Running multi-agent analysis...\n")

        response = await team.chat(task)
        result = extract_response_text(response)

        print("✓ Multi-agent analysis complete!")
        print("\n" + "=" * 80)
        print("COLLABORATIVE ANALYSIS RESULT")
        print("=" * 80)
        print(result)
        print("=" * 80)

        print("\n✅ Multi-agent NVIDIA analysis successful!\n")
        return True, result

    except Exception as e:
        print(f"\n✗ Multi-agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, ""


async def test_expert_investor_report():
    """Test Expert_Investor for report generation."""
    print("\n" + "=" * 80)
    print("EXPERT INVESTOR TEST: NVIDIA Investment Report")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import SingleAssistant
        from finrobot.agents.response_utils import extract_response_text

        print("\n🤖 Creating Expert_Investor...")
        investor = SingleAssistant("Expert_Investor")
        print("✓ Expert_Investor created\n")

        task = """
        As an Expert Investor, provide a brief investment analysis for NVIDIA (NVDA):

        1. Company Overview (1 sentence)
        2. Key Strengths (2-3 points)
        3. Key Risks (2-3 points)
        4. Investment Recommendation (Buy/Hold/Sell with brief rationale)

        Keep the analysis concise and professional.
        """

        print(f"📋 Analysis Task:")
        print(task)
        print("\n🔄 Generating investment analysis...\n")

        response = await investor.chat(task)
        result = extract_response_text(response)

        print("✓ Investment analysis complete!")
        print("\n" + "=" * 80)
        print("INVESTMENT ANALYSIS REPORT")
        print("=" * 80)
        print(result)
        print("=" * 80)

        print("\n✅ Expert_Investor report generation successful!\n")
        return True, result

    except Exception as e:
        print(f"\n✗ Expert_Investor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, ""


def save_reports_to_file(market_data, multi_agent_result, investor_report):
    """Save all analysis reports to a markdown file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    filename = report_dir / f"NVIDIA_Analysis_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# NVIDIA (NVDA) Stock Analysis Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**System**: FinRobot-AF (Microsoft Agent Framework)\n\n")
        f.write("=" * 80 + "\n\n")

        # Market Analyst Data
        f.write("## Market Analyst Analysis\n\n")
        for section_name, content in market_data:
            f.write(f"### {section_name}\n\n")
            f.write(f"{content}\n\n")

        # Multi-Agent Collaboration
        f.write("=" * 80 + "\n\n")
        f.write("## Multi-Agent Collaborative Analysis\n\n")
        f.write("**Team**: Market_Analyst, Financial_Analyst, Statistician\n\n")
        f.write(f"{multi_agent_result}\n\n")

        # Expert Investor Report
        f.write("=" * 80 + "\n\n")
        f.write("## Expert Investor Investment Report\n\n")
        f.write(f"{investor_report}\n\n")

        # Footer
        f.write("=" * 80 + "\n\n")
        f.write("**Disclaimer**: This report is generated by AI agents for educational and research purposes only. ")
        f.write("Not financial advice. Always conduct your own research before making investment decisions.\n")

    return filename


async def main():
    """Run all NVIDIA analysis tests."""
    print("\n" + "=" * 80)
    print("FINROBOT-AF REAL-WORLD TEST SUITE")
    print("NVIDIA (NVDA) Stock Analysis")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    results = []

    # Storage for report data
    market_data = []
    multi_agent_result = ""
    investor_report = ""

    # Test 1: Market_Analyst
    print("⏳ Starting Test 1: Market_Analyst Single Agent...\n")
    success, market_data = await test_market_analyst_nvda()
    results.append(("Market_Analyst Single Agent", success))

    # Test 2: Multi-Agent Collaboration
    print("⏳ Starting Test 2: Multi-Agent Collaboration...\n")
    success, multi_agent_result = await test_multi_agent_nvda_analysis()
    results.append(("Multi-Agent Collaboration", success))

    # Test 3: Expert_Investor Report
    print("⏳ Starting Test 3: Expert_Investor Report...\n")
    success, investor_report = await test_expert_investor_report()
    results.append(("Expert_Investor Report", success))

    # Summary
    print("\n" + "=" * 80)
    print("NVIDIA ANALYSIS TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("\n" + "=" * 80)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 80 + "\n")

    # Save reports to file
    if passed == total:
        print("💾 Saving analysis reports to file...\n")
        try:
            report_file = save_reports_to_file(market_data, multi_agent_result, investor_report)
            print(f"✅ Reports saved to: {report_file}\n")
        except Exception as e:
            print(f"⚠️  Failed to save reports: {e}\n")

        print("🎉 All NVIDIA analysis tests passed!")
        print("✅ FinRobot-AF successfully analyzed real stock data!")
        return 0
    else:
        print("⚠️  Some tests failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
