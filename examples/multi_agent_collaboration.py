"""
Multi-Agent Collaboration Example

This example demonstrates how multiple specialized agents can work together
to perform comprehensive financial analysis.
"""

import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import MultiAssistant, MultiAssistantWithLeader


async def example_group_chat():
    """Demonstrate multi-agent group chat."""

    print("="*80)
    print("Multi-Agent Group Chat Example")
    print("="*80)

    # Create team of specialists
    team = MultiAssistant([
        "Market_Analyst",      # Market data and trends
        "Financial_Analyst",   # Financial metrics
        "Statistician",        # Statistical analysis
    ])

    # Collaborative analysis task
    task = """
    Perform comprehensive analysis of Apple Inc. (AAPL):

    1. Market Analyst: Gather current market data, recent news, and stock performance
    2. Financial Analyst: Analyze key financial metrics and ratios
    3. Statistician: Perform statistical risk assessment and volatility analysis

    Collaborate to provide unified investment recommendation.
    """

    print("\nTask:")
    print(task)
    print("\nExecuting multi-agent collaboration...\n")

    response = await team.chat(task)

    print("\nFinal Result:")
    print("="*80)
    print(response.text)


async def example_hierarchical_workflow():
    """Demonstrate hierarchical leader-team workflow."""

    print("\n" + "="*80)
    print("Hierarchical Multi-Agent Workflow Example")
    print("="*80)

    # Create hierarchical team with leader
    workflow = MultiAssistantWithLeader(
        leader_config="Financial_Analyst",  # Leader coordinates the team
        team_configs=[
            "Market_Analyst",
            "Data_Analyst",
            "Statistician",
        ]
    )

    # Complex task requiring coordination
    task = """
    Conduct a comprehensive due diligence analysis for Microsoft (MSFT):

    As the Financial Analyst leader, coordinate your team to:
    1. Gather all relevant market and financial data
    2. Perform quantitative analysis
    3. Assess risk factors
    4. Compile findings into investment thesis

    Delegate specific tasks to team members and synthesize their findings.
    """

    print("\nTask:")
    print(task)
    print("\nExecuting hierarchical workflow...\n")

    response = await workflow.chat(task)

    print("\nFinal Result:")
    print("="*80)
    print(response.text)


async def example_specialized_team():
    """Demonstrate specialized team for specific analysis."""

    print("\n" + "="*80)
    print("Specialized Team Example: Tech Sector Analysis")
    print("="*80)

    # Create specialized team for tech sector
    team = MultiAssistant([
        "Market_Analyst",
        "Artificial_Intelligence_Engineer",
        "Data_Analyst",
    ])

    task = """
    Analyze the AI/ML sector investment opportunities:

    1. Identify top 5 companies in AI/ML space
    2. Compare their market positions and growth trajectories
    3. Evaluate technology moats and competitive advantages
    4. Provide sector-wide investment recommendations

    Focus on companies like NVDA, GOOGL, MSFT, META, AMD.
    """

    print("\nTask:")
    print(task)
    print("\nExecuting specialized team analysis...\n")

    response = await team.chat(task)

    print("\nFinal Result:")
    print("="*80)
    print(response.text)


async def main():
    """Run all multi-agent examples."""

    # Initialize configuration
    print("Initializing FinRobot configuration...")
    config = initialize_config(
        api_keys_path="config_api_keys",
        llm_config_path="OAI_CONFIG_LIST"
    )

    # Run examples
    await example_group_chat()
    await example_hierarchical_workflow()
    await example_specialized_team()


if __name__ == "__main__":
    asyncio.run(main())
