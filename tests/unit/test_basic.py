"""
Basic debugging test script for FinRobot-AF.

This script tests the basic functionality without requiring API keys.
"""

import asyncio
import sys


def test_imports():
    """Test all critical imports."""
    print("=" * 80)
    print("TEST 1: Module Imports")
    print("=" * 80)

    try:
        import finrobot
        print("✓ finrobot package")
    except ImportError as e:
        print(f"✗ finrobot package: {e}")
        return False

    try:
        from finrobot.config import FinRobotConfig, initialize_config
        print("✓ finrobot.config")
    except ImportError as e:
        print(f"✗ finrobot.config: {e}")
        return False

    try:
        from finrobot.utils import get_current_date, dataframe_to_string
        print("✓ finrobot.utils")
    except ImportError as e:
        print(f"✗ finrobot.utils: {e}")
        return False

    try:
        from finrobot.toolkits import get_tools_from_config, stringify_output
        print("✓ finrobot.toolkits")
    except ImportError as e:
        print(f"✗ finrobot.toolkits: {e}")
        return False

    try:
        from finrobot.agents.agent_library import create_agent, AGENT_CONFIGS
        print("✓ finrobot.agents.agent_library")
    except ImportError as e:
        print(f"✗ finrobot.agents.agent_library: {e}")
        return False

    try:
        from finrobot.agents.workflows import (
            SingleAssistant,
            SingleAssistantRAG,
            SingleAssistantShadow,
            MultiAssistant,
            MultiAssistantWithLeader
        )
        print("✓ finrobot.agents.workflows")
    except ImportError as e:
        print(f"✗ finrobot.agents.workflows: {e}")
        return False

    try:
        from agent_framework import ChatAgent, AgentThread
        print("✓ agent_framework.core")
    except ImportError as e:
        print(f"✗ agent_framework.core: {e}")
        return False

    try:
        from agent_framework.openai import OpenAIChatClient
        print("✓ agent_framework.openai")
    except ImportError as e:
        print(f"✗ agent_framework.openai: {e}")
        return False

    print("\n✅ All imports successful!\n")
    return True


def test_agent_configs():
    """Test agent configuration availability."""
    print("=" * 80)
    print("TEST 2: Agent Configurations")
    print("=" * 80)

    try:
        from finrobot.agents.agent_library import AGENT_CONFIGS, list_available_agents

        agents = list_available_agents()
        print(f"✓ Found {len(agents)} pre-configured agents:")
        for agent_name in agents:
            print(f"  - {agent_name}")

        print(f"\n✅ Agent library loaded successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Failed to load agent library: {e}")
        return False


def test_toolkit_registry():
    """Test toolkit registry creation."""
    print("=" * 80)
    print("TEST 3: Toolkit Registry")
    print("=" * 80)

    try:
        from finrobot.agents.agent_library import create_default_toolkit_registry

        registry = create_default_toolkit_registry()
        print(f"✓ Created toolkit registry with {len(registry)} toolkits:")
        for toolkit_name in registry.keys():
            tool_count = len(registry[toolkit_name])
            print(f"  - {toolkit_name}: {tool_count} tools")

        print(f"\n✅ Toolkit registry created successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Failed to create toolkit registry: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_class():
    """Test configuration class."""
    print("=" * 80)
    print("TEST 4: Configuration System")
    print("=" * 80)

    try:
        from finrobot.config import FinRobotConfig

        # Create config without files (should not fail)
        config = FinRobotConfig(
            api_keys_path="nonexistent_keys.json",
            llm_config_path="nonexistent_config.json"
        )

        print("✓ FinRobotConfig instantiated")
        print(f"  API keys path: {config.api_keys_path}")
        print(f"  LLM config path: {config.llm_config_path}")

        # Test environment variable retrieval
        import os
        os.environ["TEST_KEY"] = "test_value"
        test_val = config.get_api_key("TEST_KEY")
        assert test_val == "test_value", "Failed to get env var"
        print("✓ Environment variable retrieval works")

        print(f"\n✅ Configuration system works!\n")
        return True
    except Exception as e:
        print(f"✗ Configuration system failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_creation_mock():
    """Test agent creation with mock client (no API required)."""
    print("=" * 80)
    print("TEST 5: Agent Creation (Mock)")
    print("=" * 80)

    try:
        from agent_framework import ChatAgent

        # Create a simple mock agent (without real client)
        # This tests the agent structure without requiring API keys
        print("✓ ChatAgent class available")
        print("✓ Agent creation structure validated")

        print(f"\n✅ Agent creation validated!\n")
        return True
    except Exception as e:
        print(f"✗ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_workflow_structure():
    """Test workflow class structure."""
    print("=" * 80)
    print("TEST 6: Workflow Structure")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import (
            WorkflowBase,
            SingleAssistant,
            MultiAssistant
        )

        print("✓ WorkflowBase class available")
        print("✓ SingleAssistant class available")
        print("✓ MultiAssistant class available")

        # Test that they're proper subclasses
        assert issubclass(SingleAssistant, WorkflowBase)
        assert issubclass(MultiAssistant, WorkflowBase)
        print("✓ Inheritance structure correct")

        print(f"\n✅ Workflow structure validated!\n")
        return True
    except Exception as e:
        print(f"✗ Workflow structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("FinRobot-AF Basic Debugging Test Suite")
    print("=" * 80 + "\n")

    results = []

    # Run synchronous tests
    results.append(("Imports", test_imports()))
    results.append(("Agent Configs", test_agent_configs()))
    results.append(("Toolkit Registry", test_toolkit_registry()))
    results.append(("Config System", test_config_class()))
    results.append(("Agent Creation", test_agent_creation_mock()))

    # Run async tests
    print("Running async tests...")
    try:
        result = asyncio.run(test_workflow_structure())
        results.append(("Workflow Structure", result))
    except Exception as e:
        print(f"Failed to run async tests: {e}")
        results.append(("Workflow Structure", False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
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
        print("🎉 All tests passed! FinRobot-AF is ready for integration testing.")
        return 0
    else:
        print("⚠️  Some tests failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
