"""
Basic Market Analysis Example

This example demonstrates how to use FinRobot's Market_Analyst agent
to analyze stock performance and provide forecasts.
"""

import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant


async def main():
    """Run basic market analysis."""

    # Initialize configuration
    print("Initializing FinRobot configuration...")
    config = initialize_config(
        api_keys_path="config_api_keys",
        llm_config_path="OAI_CONFIG_LIST"
    )

    # Create Market Analyst
    print("\nCreating Market Analyst agent...")
    assistant = SingleAssistant("Market_Analyst")

    # Example 1: Get company profile
    print("\n" + "="*80)
    print("Example 1: Company Profile Analysis")
    print("="*80)

    response1 = await assistant.chat(
        "Get the company profile for NVIDIA (NVDA) and summarize key information"
    )
    print(f"\nResponse:\n{response1.text}")

    # Example 2: Stock price analysis
    print("\n" + "="*80)
    print("Example 2: Stock Price Analysis")
    print("="*80)

    response2 = await assistant.chat(
        "Analyze NVDA stock price performance over the last 6 months"
    )
    print(f"\nResponse:\n{response2.text}")

    # Example 3: Recent news analysis
    print("\n" + "="*80)
    print("Example 3: Recent News Analysis")
    print("="*80)

    response3 = await assistant.chat(
        "Get recent news for NVDA and analyze sentiment"
    )
    print(f"\nResponse:\n{response3.text}")

    # Example 4: Comprehensive forecast
    print("\n" + "="*80)
    print("Example 4: Comprehensive Market Forecast")
    print("="*80)

    response4 = await assistant.chat(
        "Based on company financials, recent news, and stock performance, "
        "provide a comprehensive forecast for NVDA for the next quarter"
    )
    print(f"\nResponse:\n{response4.text}")

    # Reset conversation for new analysis
    print("\n" + "="*80)
    print("Resetting conversation state...")
    assistant.reset()

    # Example 5: Different stock
    print("\n" + "="*80)
    print("Example 5: Analyzing Different Stock")
    print("="*80)

    response5 = await assistant.chat(
        "Analyze Tesla (TSLA) stock and provide investment recommendation"
    )
    print(f"\nResponse:\n{response5.text}")


if __name__ == "__main__":
    asyncio.run(main())
