"""
Investment Report Generation Example

This example demonstrates how to use the Expert_Investor agent with
shadow planning to generate comprehensive financial analysis reports.
"""

import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistantShadow


async def generate_annual_report():
    """Generate comprehensive annual report analysis."""

    print("="*80)
    print("Annual Report Generation Example")
    print("="*80)

    # Initialize configuration
    config = initialize_config(
        api_keys_path="config_api_keys",
        llm_config_path="OAI_CONFIG_LIST"
    )

    # Create Expert Investor with shadow planning
    print("\nCreating Expert Investor agent with shadow planner...")
    assistant = SingleAssistantShadow("Expert_Investor")

    # Define report requirements
    task = """
    Generate a comprehensive investment analysis report for Apple Inc. (AAPL) with the following sections:

    1. Executive Summary
       - Company overview
       - Key investment highlights
       - Overall recommendation

    2. Financial Analysis
       - Retrieve latest SEC 10-K filing
       - Analyze income statement, balance sheet, and cash flow
       - Calculate key financial ratios (P/E, ROE, Debt-to-Equity, etc.)
       - Year-over-year growth trends

    3. Market Position
       - Industry analysis
       - Competitive landscape
       - Market share and positioning

    4. Risk Assessment
       - Business risks
       - Market risks
       - Financial risks

    5. Valuation
       - Current valuation metrics
       - Comparison to industry peers
       - Fair value estimation

    6. Investment Thesis
       - Bull case
       - Bear case
       - Base case scenario

    7. Recommendation
       - Investment rating (Buy/Hold/Sell)
       - Target price
       - Time horizon

    Please use available tools to gather data and create detailed charts where appropriate.
    Save the final report as a PDF document.
    """

    print("\nTask:")
    print(task)
    print("\n" + "="*80)
    print("Executing report generation workflow...")
    print("(This may take several minutes)")
    print("="*80 + "\n")

    # Execute with shadow planning
    response = await assistant.chat(task)

    print("\nReport Generation Complete!")
    print("="*80)
    print(response.text)


async def generate_sector_comparison():
    """Generate sector comparison report."""

    print("\n" + "="*80)
    print("Sector Comparison Report Example")
    print("="*80)

    # Create Expert Investor
    assistant = SingleAssistantShadow("Expert_Investor")

    task = """
    Create a comparative analysis report for the top 3 tech companies:
    Apple (AAPL), Microsoft (MSFT), and Google (GOOGL)

    Compare the following aspects:
    1. Financial Performance (last 3 years)
    2. Profitability Metrics
    3. Growth Rates
    4. Valuation Multiples
    5. Balance Sheet Strength
    6. Cash Flow Generation

    Create comparison charts for key metrics.
    Provide investment ranking and recommendations.
    """

    print("\nTask:")
    print(task)
    print("\nExecuting sector comparison...\n")

    response = await assistant.chat(task)

    print("\nSector Comparison Complete!")
    print("="*80)
    print(response.text)


async def generate_quarterly_update():
    """Generate quarterly earnings update."""

    print("\n" + "="*80)
    print("Quarterly Earnings Update Example")
    print("="*80)

    assistant = SingleAssistantShadow("Expert_Investor")

    task = """
    Analyze the latest quarterly earnings for NVIDIA (NVDA):

    1. Retrieve recent earnings report and earnings call transcript
    2. Extract key financial metrics:
       - Revenue and growth
       - EPS (actual vs. expected)
       - Gross margin trends
       - Operating expenses
       - Guidance for next quarter

    3. Analyze management commentary:
       - Key strategic initiatives
       - Market outlook
       - Challenges and opportunities

    4. Market reaction:
       - Stock price movement post-earnings
       - Analyst reactions
       - Price target changes

    5. Investment implications:
       - Update investment thesis
       - Revise price target if needed
       - Recommendation update

    Create visualizations of key trends and compile into concise report.
    """

    print("\nTask:")
    print(task)
    print("\nExecuting quarterly update analysis...\n")

    response = await assistant.chat(task)

    print("\nQuarterly Update Complete!")
    print("="*80)
    print(response.text)


async def main():
    """Run all report generation examples."""

    # Choose which examples to run
    print("Investment Report Generation Examples\n")
    print("Select example to run:")
    print("1. Annual Report (comprehensive)")
    print("2. Sector Comparison")
    print("3. Quarterly Earnings Update")
    print("4. All examples (sequential)")

    # For demo purposes, run a simple example
    # In production, you can add user input here

    # Run annual report example
    await generate_annual_report()

    # Uncomment to run other examples
    # await generate_sector_comparison()
    # await generate_quarterly_update()


if __name__ == "__main__":
    asyncio.run(main())
