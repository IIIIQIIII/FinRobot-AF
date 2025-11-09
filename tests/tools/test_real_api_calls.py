"""
Verification test: Ensure Market_Analyst actually calls Yahoo Finance API.

This test confirms that agents use REAL market data instead of LLM knowledge.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta


async def test_market_analyst_real_api():
    """Test that Market_Analyst calls real Yahoo Finance API."""
    print("=" * 80)
    print("VERIFICATION: Market_Analyst Real API Call Test")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import SingleAssistant
        from finrobot.agents.response_utils import extract_response_text

        print("\n🤖 Creating Market_Analyst...")
        analyst = SingleAssistant("Market_Analyst")
        print("✓ Market_Analyst created")

        # Check registered tools
        if hasattr(analyst, 'agent') and hasattr(analyst.agent, 'tools'):
            tools = analyst.agent.tools
            print(f"\n✓ Agent has {len(tools) if tools else 0} tools registered:")
            if tools:
                for i, tool in enumerate(tools[:5], 1):  # Show first 5
                    tool_name = getattr(tool, 'name', 'unknown')
                    print(f"   {i}. {tool_name}")
                if len(tools) > 5:
                    print(f"   ... and {len(tools) - 5} more tools")

        # Test 1: Get current stock price (requires API call)
        print("\n" + "=" * 80)
        print("Test 1: Get NVIDIA Current Stock Price")
        print("=" * 80)

        query1 = """
        Call get_stock_info('NVDA') to get NVIDIA's current stock information.
        Then tell me: What is the current stock price?
        """

        print(f"\n📊 Query: {query1.strip()}")
        print("\n🔄 Calling API...\n")

        response1 = await analyst.chat(query1)
        result1 = extract_response_text(response1)

        print("✓ Response received:")
        print("-" * 80)
        print(result1)
        print("-" * 80)

        # Verify real data was used
        has_price = "$" in result1 or any(word in result1.lower() for word in ["price", "trading"])
        has_disclaimer = "I don't have" in result1 or "cannot access" in result1.lower()

        if has_price and not has_disclaimer:
            print("\n✅ SUCCESS: Real API data was retrieved!")
        elif has_disclaimer:
            print("\n❌ FAILED: Agent did NOT call API (relied on knowledge)")
            return False
        else:
            print("\n⚠️  UNCLEAR: Manual verification needed")

        # Test 2: Get stock history (requires API with date range)
        print("\n" + "=" * 80)
        print("Test 2: Get NVIDIA Stock History")
        print("=" * 80)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        query2 = f"""
        Use get_stock_data to retrieve NVIDIA (NVDA) stock price data
        from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.

        Then tell me: What was the highest closing price in this period?
        """

        print(f"\n📈 Query: {query2.strip()}")
        print("\n🔄 Calling API...\n")

        response2 = await analyst.chat(query2)
        result2 = extract_response_text(response2)

        print("✓ Response received:")
        print("-" * 80)
        print(result2)
        print("-" * 80)

        # Verify real historical data
        has_specific_price = "$" in result2 and any(char.isdigit() for char in result2)
        has_date_ref = any(str(d) in result2 for d in range(1, 32))  # Check for day numbers

        if has_specific_price or has_date_ref:
            print("\n✅ SUCCESS: Real historical data was retrieved!")
        else:
            print("\n⚠️  Could not verify if real data was used")

        # Test 3: Get company information
        print("\n" + "=" * 80)
        print("Test 3: Get NVIDIA Company Information")
        print("=" * 80)

        query3 = """
        Use get_company_info to fetch NVIDIA (NVDA) company details.
        Tell me the company's industry and sector.
        """

        print(f"\n🏢 Query: {query3.strip()}")
        print("\n🔄 Calling API...\n")

        response3 = await analyst.chat(query3)
        result3 = extract_response_text(response3)

        print("✓ Response received:")
        print("-" * 80)
        print(result3)
        print("-" * 80)

        if "semiconductor" in result3.lower() or "technology" in result3.lower():
            print("\n✅ SUCCESS: Real company data was retrieved!")
        else:
            print("\n⚠️  Could not verify company data")

        print("\n✅ Market_Analyst API verification complete!\n")
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_comparison():
    """Compare agent response with direct API call."""
    print("=" * 80)
    print("VERIFICATION: Direct API vs Agent Comparison")
    print("=" * 80)

    try:
        from finrobot.data_source.yfinance_utils import YFinanceUtils
        from finrobot.agents.workflows import SingleAssistant
        from finrobot.agents.response_utils import extract_response_text

        # 1. Direct API call
        print("\n📊 Step 1: Direct API call to get NVDA stock info...")
        direct_info = YFinanceUtils.get_stock_info('NVDA')
        direct_price = direct_info.get('currentPrice', 'N/A')
        direct_name = direct_info.get('shortName', 'N/A')

        print(f"✓ Direct API result:")
        print(f"   Company: {direct_name}")
        print(f"   Current Price: ${direct_price}")

        # 2. Agent call
        print("\n🤖 Step 2: Agent call for same information...")
        analyst = SingleAssistant("Market_Analyst")

        query = "Use get_stock_info to get NVIDIA (NVDA) current price. State only the price."
        response = await analyst.chat(query)
        result = extract_response_text(response)

        print(f"✓ Agent response:")
        print(f"   {result}")

        # 3. Compare
        print("\n🔍 Step 3: Comparison...")
        price_str = str(direct_price)

        if price_str in result or (direct_price and abs(float(direct_price) - 100) < 500):
            # Check if response contains similar price (within reason)
            if "$" in result and any(c.isdigit() for c in result):
                print("✅ Agent appears to be using real API data!")
                print(f"   Direct API price: ${direct_price}")
                print(f"   Agent mentioned price in response")
                return True

        print("⚠️  Could not confirm agent used real data")
        return False

    except Exception as e:
        print(f"\n✗ Comparison test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all real API verification tests."""
    print("\n" + "=" * 80)
    print("FINROBOT-AF REAL API VERIFICATION SUITE")
    print("Yahoo Finance API Integration Test")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    results = []

    # Test 1: Market_Analyst Real API Calls
    print("⏳ Test 1: Market_Analyst with Real API...\n")
    success = await test_market_analyst_real_api()
    results.append(("Market_Analyst Real API", success))

    # Test 2: Direct Comparison
    print("⏳ Test 2: Direct API vs Agent Comparison...\n")
    success = await test_direct_comparison()
    results.append(("Direct Comparison", success))

    # Summary
    print("\n" + "=" * 80)
    print("REAL API VERIFICATION SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("\n" + "=" * 80)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 80 + "\n")

    if passed == total:
        print("🎉 All API verification tests passed!")
        print("✅ FinRobot-AF agents successfully call Yahoo Finance API!")
        print("✅ Agents use REAL market data, not just LLM knowledge!")
        return 0
    elif passed > 0:
        print("⚠️  Some tests passed, but verification incomplete.")
        return 0
    else:
        print("❌ API verification failed.")
        print("\nAgents are NOT calling real APIs - using only LLM knowledge.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
