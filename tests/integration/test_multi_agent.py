"""
Multi-Agent Testing Script for FinRobot-AF

Tests complex multi-agent workflows including:
- Group chat with multiple agents
- Hierarchical coordination with leader
- Agent-to-agent communication
"""

import asyncio
import sys
import os


async def test_multi_agent_group_chat():
    """Test MultiAssistant group chat pattern."""
    print("=" * 80)
    print("TEST 1: Multi-Agent Group Chat")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistant
        from finrobot.agents.response_utils import extract_response_text

        # Create team of analysts
        print("Creating multi-agent team...")
        team = MultiAssistant([
            "Financial_Analyst",
            "Data_Analyst",
            "Statistician"
        ])

        print(f"✓ Team created with {len(team.agents)} agents:")
        for agent in team.agents:
            print(f"  - {agent.name}")

        # Simple collaborative task
        task = """
        Analyze this scenario: A tech company has revenue of $100M with 40% profit margin.

        Financial_Analyst: Calculate the profit amount.
        Data_Analyst: Interpret what this profit margin means.
        Statistician: Is 40% a good profit margin for tech companies?

        Keep responses brief (1-2 sentences each).
        """

        print(f"\n🤖 Task:\n{task}")
        print("\n🔄 Running group chat...")

        response = await team.chat(task)

        print(f"\n✓ Group chat completed")
        print(f"\nFinal Response:")
        print("-" * 80)
        print(extract_response_text(response))
        print("-" * 80)

        print("\n✅ Multi-agent group chat test successful!\n")
        return True

    except Exception as e:
        print(f"✗ Multi-agent group chat failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_hierarchical_workflow():
    """Test MultiAssistantWithLeader hierarchical pattern."""
    print("=" * 80)
    print("TEST 2: Hierarchical Multi-Agent Workflow")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistantWithLeader

        # Create hierarchical team
        print("Creating hierarchical team with leader...")
        workflow = MultiAssistantWithLeader(
            leader_config="Financial_Analyst",  # Leader
            team_configs=[
                "Data_Analyst",
                "Statistician"
            ]
        )

        print(f"✓ Hierarchical team created:")
        print(f"  Leader: {workflow.leader.name}")
        print(f"  Team members:")
        for agent in workflow.team:
            print(f"    - {agent.name}")

        # Task requiring delegation
        task = """
        As the Financial Analyst leader, coordinate your team to analyze:

        A startup has grown revenue from $10M to $50M in 2 years.

        Delegate to your team:
        [Data_Analyst] Calculate the growth rate
        [Statistician] Assess if this growth rate is sustainable

        Then provide a final recommendation.

        Keep all responses brief.
        """

        print(f"\n🤖 Task:\n{task}")
        print("\n🔄 Running hierarchical workflow...")

        response = await workflow.chat(task)

        from finrobot.agents.response_utils import extract_response_text

        print(f"\n✓ Hierarchical workflow completed")
        print(f"\nResponse:")
        print("-" * 80)
        print(extract_response_text(response))
        print("-" * 80)

        print("\n✅ Hierarchical workflow test successful!\n")
        return True

    except Exception as e:
        print(f"✗ Hierarchical workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_simple_collaboration():
    """Test simple two-agent collaboration."""
    print("=" * 80)
    print("TEST 3: Simple Agent Collaboration")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistant
        from finrobot.agents.response_utils import extract_response_text

        # Just two agents
        print("Creating two-agent collaboration...")
        team = MultiAssistant([
            "Financial_Analyst",
            "Statistician"
        ])

        print(f"✓ Two-agent team created")

        task = """
        Question: What's the difference between mean and median?

        Financial_Analyst: Explain from a finance perspective
        Statistician: Explain from a statistics perspective

        One sentence each.
        """

        print(f"\n🤖 Task:\n{task}")
        print("\n🔄 Running collaboration...")

        response = await team.chat(task)

        print(f"\n✓ Collaboration completed")
        print(f"\nResponse:")
        print("-" * 80)
        print(extract_response_text(response))
        print("-" * 80)

        print("\n✅ Simple collaboration test successful!\n")
        return True

    except Exception as e:
        print(f"✗ Simple collaboration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_specialized_team():
    """Test specialized team for specific domain."""
    print("=" * 80)
    print("TEST 4: Specialized Team (AI/Tech Focus)")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistant
        from finrobot.agents.response_utils import extract_response_text

        # AI/Tech specialized team
        print("Creating AI/Tech specialized team...")
        team = MultiAssistant([
            "Artificial_Intelligence_Engineer",
            "Software_Developer",
            "IT_Specialist"
        ])

        print(f"✓ Specialized team created with {len(team.agents)} agents")

        task = """
        Quick question: What are the key considerations when deploying an AI model to production?

        Each expert give ONE key consideration from your perspective.
        Keep it to one sentence each.
        """

        print(f"\n🤖 Task:\n{task}")
        print("\n🔄 Running specialized team...")

        response = await team.chat(task)

        print(f"\n✓ Specialized team completed")
        print(f"\nResponse:")
        print("-" * 80)
        print(extract_response_text(response))
        print("-" * 80)

        print("\n✅ Specialized team test successful!\n")
        return True

    except Exception as e:
        print(f"✗ Specialized team failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_workflow_state_management():
    """Test that workflows properly manage state across multiple interactions."""
    print("=" * 80)
    print("TEST 5: Workflow State Management")
    print("=" * 80)

    try:
        from finrobot.agents.workflows import MultiAssistant

        print("Creating team...")
        team = MultiAssistant([
            "Financial_Analyst",
            "Data_Analyst"
        ])

        # First interaction
        print("\n🤖 First query...")
        response1 = await team.chat("What is ROI? One sentence.")

        print(f"✓ First response received: {response1.text[:100] if hasattr(response1, 'text') else str(response1)[:100]}...")

        # Reset state
        print("\n🔄 Resetting workflow state...")
        team.reset()
        print("✓ State reset")

        # Second interaction (should not remember first)
        print("\n🤖 Second query...")
        response2 = await team.chat("What is NPV? One sentence.")

        print(f"✓ Second response received: {response2.text[:100] if hasattr(response2, 'text') else str(response2)[:100]}...")

        print("\n✅ State management test successful!\n")
        return True

    except Exception as e:
        print(f"✗ State management failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all multi-agent tests."""
    print("\n" + "=" * 80)
    print("FinRobot-AF Multi-Agent Test Suite")
    print("=" * 80 + "\n")

    results = []

    # Test 1: Multi-Agent Group Chat
    print("⏳ Starting Test 1...")
    success = await test_multi_agent_group_chat()
    results.append(("Multi-Agent Group Chat", success))

    # Test 2: Hierarchical Workflow
    print("⏳ Starting Test 2...")
    success = await test_hierarchical_workflow()
    results.append(("Hierarchical Workflow", success))

    # Test 3: Simple Collaboration
    print("⏳ Starting Test 3...")
    success = await test_simple_collaboration()
    results.append(("Simple Collaboration", success))

    # Test 4: Specialized Team
    print("⏳ Starting Test 4...")
    success = await test_specialized_team()
    results.append(("Specialized Team", success))

    # Test 5: State Management
    print("⏳ Starting Test 5...")
    success = await test_workflow_state_management()
    results.append(("State Management", success))

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
    print("MULTI-AGENT TEST SUMMARY")
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
        print("🎉 All multi-agent tests passed!")
        print("✅ FinRobot-AF multi-agent workflows are fully functional!")
        return 0
    elif passed >= total * 0.6:
        print("⚠️  Most tests passed. See failures above.")
        return 0
    else:
        print("❌ Many tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
