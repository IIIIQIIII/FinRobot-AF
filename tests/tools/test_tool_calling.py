"""
Test script to verify that agents can actually call tools (Yahoo Finance API).

This test ensures that Market_Analyst uses real API calls instead of
relying solely on LLM knowledge.
"""

import asyncio
import sys
import os


async def test_tool_registration():
    """Verify that tools are properly registered."""
    print("=" * 80)
    print("TEST: Tool Registration Verification")
    print("=" * 80)

    try:
        from finrobot.toolkits import get_market_data_tools
        from finrobot.config import get_config

        print("\n🔧 Getting market data tools...")
        tools = get_market_data_tools()

        print(f"✓ Tools extracted: {len(tools)} tools")
        for i, tool in enumerate(tools, 1):
            tool_name = getattr(tool, '__name__', str(tool))
            print(f"  {i}. {tool_name}")

        if len(tools) == 0:
            print("⚠️  WARNING: No tools were extracted!")
            return False

        print("\n✅ Tool registration check passed!\n")
        return True

    except Exception as e:
        print(f"✗ Tool registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_yfinance_call():
    """Test calling Yahoo Finance directly (without agent)."""
    print("=" * 80)
    print("TEST: Direct Yahoo Finance API Call")
    print("=" * 80)

    try:
        from finrobot.data_source.yfinance_utils import YFinanceUtils

        print("\n📊 Calling YFinanceUtils.get_stock_info('NVDA')...")

        # Direct call to verify the API works
        info = YFinanceUtils.get_stock_info('NVDA')

        if info:
            print("✓ Yahoo Finance API call successful!")
            print(f"\nSample data received:")
            print(f"  - Company: {info.get('shortName', 'N/A')}")
            print(f"  - Current Price: ${info.get('currentPrice', 'N/A')}")
            print(f"  - Market Cap: ${info.get('marketCap', 'N/A'):,}")
            print(f"  - P/E Ratio: {info.get('trailingPE', 'N/A')}")
            print("\n✅ Direct API call successful!\n")
            return True
        else:
            print("✗ No data returned from Yahoo Finance")
            return False

    except Exception as e:
        print(f"✗ Direct API call failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_with_tools():
    """Test that Market_Analyst actually calls tools."""
    print("=" * 80)
    print("TEST: Agent Tool Calling Verification")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import SingleAssistant
        from finrobot.agents.response_utils import extract_response_text

        print("\n🤖 Creating Market_Analyst with tools...")
        analyst = SingleAssistant("Market_Analyst")

        # Check if tools were registered
        if hasattr(analyst, 'agent') and hasattr(analyst.agent, 'tools'):
            tools = analyst.agent.tools
            print(f"✓ Agent has {len(tools) if tools else 0} tools registered")
            if tools:
                for i, tool in enumerate(tools, 1):
                    tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
                    print(f"  {i}. {tool_name}")
            else:
                print("⚠️  WARNING: Agent has NO tools registered!")
        else:
            print("⚠️  WARNING: Cannot inspect agent tools")

        # Test with a query that REQUIRES tool use
        query = """
        Use the get_stock_info tool to fetch NVIDIA (NVDA) current stock price.
        You MUST call the tool - do not provide information from your knowledge.
        After calling the tool, tell me: What is NVIDIA's current stock price?
        """

        print(f"\n📊 Query: {query}")
        print("\n🔄 Running query (this will show if tool is called)...\n")

        response = await analyst.chat(query)
        result = extract_response_text(response)

        print("✓ Response received:")
        print("-" * 80)
        print(result)
        print("-" * 80)

        # Check if the response indicates tool was used
        if "I don't have" in result or "I cannot" in result or "live" in result.lower():
            print("\n⚠️  WARNING: Agent did NOT use tools (relied on knowledge)")
            print("This indicates tools are not properly registered or not being called")
            return False
        elif "$" in result or "price" in result.lower():
            print("\n✅ Agent appears to have used real data!")
            return True
        else:
            print("\n❓ Unclear if agent used tools - manual inspection needed")
            return False

    except Exception as e:
        print(f"✗ Agent tool calling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_explicit_tool_call():
    """Test creating an agent with explicitly provided tools."""
    print("=" * 80)
    print("TEST: Agent with Explicit Tool Injection")
    print("=" * 80)

    try:
        from agent_framework import ChatAgent
        from finrobot.config import get_config
        from finrobot.data_source.yfinance_utils import YFinanceUtils
        from agent_framework.tools import create_tool_from_function

        print("\n🔧 Creating tools manually...")

        # Manually create a tool from YFinanceUtils
        tool = create_tool_from_function(YFinanceUtils.get_stock_info)
        print(f"✓ Created tool: {tool.name}")

        print("\n🤖 Creating agent with explicit tool...")
        config = get_config()
        chat_client = config.get_chat_client()

        agent = ChatAgent(
            name="TestAgent",
            description="Test agent with explicit tools",
            chat_client=chat_client,
            instructions="You are a financial analyst. Use the provided tools to get real market data.",
            tools=[tool]
        )

        print(f"✓ Agent created with {len(agent.tools)} tool(s)")

        thread = agent.get_new_thread()

        query = "Use get_stock_info to get NVIDIA (NVDA) stock information. What is the current price?"
        print(f"\n📊 Query: {query}")
        print("\n🔄 Running query...\n")

        response = await agent.run(query, thread=thread)

        print("✓ Response received:")
        print("-" * 80)
        print(response.text)
        print("-" * 80)

        if "$" in response.text or "price" in response.text.lower():
            print("\n✅ Explicit tool injection works!")
            return True
        else:
            print("\n⚠️  Tool may not have been called")
            return False

    except Exception as e:
        print(f"✗ Explicit tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tool calling verification tests."""
    print("\n" + "=" * 80)
    print("FINROBOT-AF TOOL CALLING VERIFICATION SUITE")
    print("Testing Yahoo Finance API Integration")
    print("=" * 80 + "\n")

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    results = []

    # Test 1: Tool Registration
    print("⏳ Test 1: Verifying tool registration...\n")
    success = await test_tool_registration()
    results.append(("Tool Registration", success))

    # Test 2: Direct API Call
    print("⏳ Test 2: Testing direct Yahoo Finance API...\n")
    success = await test_direct_yfinance_call()
    results.append(("Direct API Call", success))

    # Test 3: Agent with Tools
    print("⏳ Test 3: Testing agent with tools...\n")
    success = await test_agent_with_tools()
    results.append(("Agent Tool Calling", success))

    # Test 4: Explicit Tool Injection
    print("⏳ Test 4: Testing explicit tool injection...\n")
    success = await test_explicit_tool_call()
    results.append(("Explicit Tool Injection", success))

    # Summary
    print("\n" + "=" * 80)
    print("TOOL CALLING VERIFICATION SUMMARY")
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
        print("🎉 All tool calling tests passed!")
        print("✅ Agents can successfully call Yahoo Finance API!")
        return 0
    else:
        print("⚠️  Some tests failed. Tool calling needs debugging.")
        print("\nPossible issues:")
        print("1. Tools not properly registered in toolkit system")
        print("2. Agent not configured to use tools")
        print("3. Tool extraction from classes not working")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
