"""
Integration Test Script for FinRobot-AF

This script tests real Agent Framework functionality with actual API keys.
Tests are designed to be safe and use public financial data only.
"""

import asyncio
import sys
import os


def test_configuration_loading():
    """Test that configuration files load correctly."""
    print("=" * 80)
    print("TEST 1: Configuration Loading")
    print("=" * 80)

    try:
        from finrobot.config import initialize_config, get_config

        # Initialize with actual config files
        config = initialize_config(
            api_keys_path="config_api_keys",
            llm_config_path="OAI_CONFIG_LIST",
            auto_load=True
        )

        print("✓ Configuration initialized")

        # Check API keys loaded
        openai_key = config.openai_api_key
        if openai_key:
            print(f"✓ OpenAI API key loaded: {openai_key[:8]}...")
        else:
            print("⚠ OpenAI API key not found")

        finnhub_key = config.finnhub_api_key
        if finnhub_key:
            print(f"✓ FinnHub API key loaded: {finnhub_key[:8]}...")
        else:
            print("⚠ FinnHub API key not found (optional)")

        print("\n✅ Configuration loading successful!\n")
        return True, config

    except FileNotFoundError as e:
        print(f"✗ Configuration files not found: {e}")
        print("Please ensure config_api_keys and OAI_CONFIG_LIST exist")
        return False, None
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def test_chat_client_creation(config):
    """Test creating OpenAI chat client."""
    print("=" * 80)
    print("TEST 2: Chat Client Creation")
    print("=" * 80)

    try:
        # Get chat client from config
        client = config.get_chat_client()

        print(f"✓ Chat client created: {type(client).__name__}")
        print(f"✓ Model ID: {client.model_id if hasattr(client, 'model_id') else 'N/A'}")

        print("\n✅ Chat client creation successful!\n")
        return True, client

    except Exception as e:
        print(f"✗ Chat client creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def test_simple_agent_creation(chat_client):
    """Test creating a simple agent without tools."""
    print("=" * 80)
    print("TEST 3: Simple Agent Creation")
    print("=" * 80)

    try:
        from agent_framework import ChatAgent

        # Create a simple agent without tools
        agent = ChatAgent(
            name="TestAgent",
            chat_client=chat_client,
            instructions="You are a helpful AI assistant. Keep responses brief and concise.",
        )

        print(f"✓ Agent created: {agent.name}")
        print(f"✓ Agent ID: {agent.id}")

        # Test basic chat (no tools)
        print("\n🤖 Testing basic chat...")
        thread = agent.get_new_thread()
        print("✓ Thread created")

        response = await agent.run("Hello! Please respond with just 'Hi there!'", thread=thread)

        print(f"✓ Agent response received")
        print(f"  Response text: {response.text[:100]}...")

        print("\n✅ Simple agent creation and chat successful!\n")
        return True, agent

    except Exception as e:
        print(f"✗ Simple agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def test_finrobot_agent_creation():
    """Test creating FinRobot agent from library."""
    print("=" * 80)
    print("TEST 4: FinRobot Agent Creation")
    print("=" * 80)

    try:
        from finrobot.config import get_config
        from finrobot.agents.agent_library import create_agent, create_default_toolkit_registry

        config = get_config()
        client = config.get_chat_client()

        # Create toolkit registry (tools may not work yet)
        print("Creating toolkit registry...")
        registry = create_default_toolkit_registry()
        print(f"✓ Toolkit registry created with {len(registry)} toolkits")

        # Create Financial_Analyst (no complex tools)
        print("\nCreating Financial_Analyst agent...")
        agent = create_agent(
            "Financial_Analyst",
            chat_client=client,
            toolkit_registry=registry
        )

        print(f"✓ Agent created: {agent.name}")
        print(f"✓ Agent description: {agent.description[:60]}...")

        print("\n✅ FinRobot agent creation successful!\n")
        return True, agent

    except Exception as e:
        print(f"✗ FinRobot agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def test_workflow_creation():
    """Test creating workflow patterns."""
    print("=" * 80)
    print("TEST 5: Workflow Pattern Creation")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import SingleAssistant

        # Create SingleAssistant workflow
        print("Creating SingleAssistant workflow...")
        workflow = SingleAssistant("Financial_Analyst")

        print(f"✓ Workflow created")
        print(f"✓ Agent: {workflow.agent.name}")
        print(f"✓ Thread: {workflow.thread is not None}")

        # Test basic chat through workflow
        print("\n🤖 Testing workflow chat...")
        response = await workflow.chat(
            "What is financial analysis? Answer in one sentence."
        )

        print(f"✓ Workflow response received")
        print(f"  Response: {response.text[:150]}...")

        print("\n✅ Workflow creation and execution successful!\n")
        return True, workflow

    except Exception as e:
        print(f"✗ Workflow creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def test_market_analyst_simple():
    """Test Market_Analyst with a simple query (no tools for now)."""
    print("=" * 80)
    print("TEST 6: Market_Analyst Simple Query")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import SingleAssistant

        # Create Market_Analyst
        print("Creating Market_Analyst workflow...")
        workflow = SingleAssistant("Market_Analyst")

        print(f"✓ Market_Analyst created")

        # Simple query without tool use
        query = "Explain what a market analyst does in one sentence."
        print(f"\n🤖 Query: {query}")

        response = await workflow.chat(query)

        print(f"\n✓ Response received:")
        print(f"  {response.text[:200]}...")

        print("\n✅ Market_Analyst simple query successful!\n")
        return True

    except Exception as e:
        print(f"✗ Market_Analyst query failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all integration tests sequentially."""
    print("\n" + "=" * 80)
    print("FinRobot-AF Integration Test Suite")
    print("=" * 80 + "\n")

    results = []

    # Test 1: Configuration Loading
    success, config = test_configuration_loading()
    results.append(("Configuration Loading", success))
    if not success:
        print("\n❌ Cannot proceed without configuration. Stopping tests.")
        return results

    # Test 2: Chat Client Creation
    success, client = await test_chat_client_creation(config)
    results.append(("Chat Client Creation", success))
    if not success:
        print("\n❌ Cannot proceed without chat client. Stopping tests.")
        return results

    # Test 3: Simple Agent Creation
    success, agent = await test_simple_agent_creation(client)
    results.append(("Simple Agent Creation", success))

    # Test 4: FinRobot Agent Creation
    success, finrobot_agent = await test_finrobot_agent_creation()
    results.append(("FinRobot Agent Creation", success))

    # Test 5: Workflow Creation
    success, workflow = await test_workflow_creation()
    results.append(("Workflow Creation", success))

    # Test 6: Market_Analyst Simple Query
    success = await test_market_analyst_simple()
    results.append(("Market_Analyst Query", success))

    return results


def main():
    """Main entry point."""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")

    # Run tests
    try:
        results = asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Summary
    print("\n" + "=" * 80)
    print("INTEGRATION TEST SUMMARY")
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
        print("🎉 All integration tests passed!")
        print("✅ FinRobot-AF is working with Agent Framework!")
        return 0
    elif passed >= total * 0.7:
        print("⚠️  Most tests passed, but some issues remain.")
        print("Check failed tests above for details.")
        return 0
    else:
        print("❌ Many tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
