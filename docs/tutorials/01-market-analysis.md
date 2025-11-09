# Tutorial 1: Market Analysis with FinRobot

Learn how to perform market analysis using FinRobot's Market Analyst agent.

## Overview

In this tutorial, you'll learn to:
- Create a Market Analyst agent
- Retrieve real-time stock data
- Analyze market trends
- Generate price forecasts
- Create visualizations

**Time**: 15-20 minutes
**Difficulty**: Beginner

## Prerequisites

- FinRobot-AF installed
- Configuration files setup (`OAI_CONFIG_LIST`, `config_api_keys`)
- Basic Python knowledge
- Understanding of async/await

## Step 1: Setup

Create a new Python file `market_analysis_tutorial.py`:

```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

# Initialize configuration
config = initialize_config(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)

print("✓ Configuration loaded")
```

## Step 2: Create Market Analyst

```python
async def main():
    # Create Market Analyst agent
    analyst = SingleAssistant("Market_Analyst")
    print("✓ Market Analyst created")

    # Test with simple query
    response = await analyst.chat("Hello, can you help me analyze stocks?")
    print(f"\nAgent: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Run it**:
```bash
python market_analysis_tutorial.py
```

**Expected Output**:
```
✓ Configuration loaded
✓ Market Analyst created

Agent: Hello! Yes, I can help you analyze stocks. I have access to real-time
market data, company profiles, financial news, and can perform technical analysis...
```

## Step 3: Get Stock Price

```python
async def get_stock_price():
    analyst = SingleAssistant("Market_Analyst")

    # Query current stock price
    response = await analyst.chat(
        "What is the current stock price of Apple (AAPL)?"
    )

    print(f"\n{response.text}")

asyncio.run(get_stock_price())
```

**Sample Output**:
```
The current stock price of Apple (AAPL) is $178.45.
```

## Step 4: Multi-turn Analysis

```python
async def multi_turn_analysis():
    analyst = SingleAssistant("Market_Analyst")

    # First query: Get price
    response1 = await analyst.chat(
        "What is the current price of NVIDIA (NVDA)?"
    )
    print(f"\nQ1: {response1.text}")

    # Second query: Get change (agent remembers context)
    response2 = await analyst.chat(
        "What was the price change from yesterday?"
    )
    print(f"\nQ2: {response2.text}")

    # Third query: Forecast
    response3 = await analyst.chat(
        "Based on recent trends, what's your short-term forecast?"
    )
    print(f"\nQ3: {response3.text}")

asyncio.run(multi_turn_analysis())
```

**Key Concept**: The agent maintains conversation context through the thread.

## Step 5: Comprehensive Stock Analysis

```python
async def comprehensive_analysis(symbol: str):
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Perform a comprehensive analysis of {symbol}:
    1. Current stock price
    2. 50-day and 200-day moving averages
    3. Recent price trend (last month)
    4. Key company news
    5. Short-term price forecast
    """

    response = await analyst.chat(query)
    print(f"\n{'='*60}")
    print(f"Analysis for {symbol}")
    print('='*60)
    print(response.text)
    print('='*60)

# Analyze Apple
asyncio.run(comprehensive_analysis("AAPL"))
```

## Step 6: Compare Multiple Stocks

```python
async def compare_stocks(symbols: list):
    analyst = SingleAssistant("Market_Analyst")

    symbols_str = ", ".join(symbols)
    query = f"""
    Compare these stocks: {symbols_str}

    For each stock, provide:
    - Current price
    - Day's price change (% and $)
    - 1-month performance
    - Brief outlook

    Then provide a ranking based on short-term potential.
    """

    response = await analyst.chat(query)
    print(f"\n{response.text}")

# Compare tech stocks
asyncio.run(compare_stocks(["AAPL", "MSFT", "GOOGL", "AMZN"]))
```

## Step 7: Sector Analysis

```python
async def sector_analysis(sector: str):
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Analyze the {sector} sector:
    1. Overall sector performance this month
    2. Top 3 performing stocks in the sector
    3. Key trends driving the sector
    4. Major news impacting the sector
    5. Sector outlook for next quarter
    """

    response = await analyst.chat(query)
    print(f"\n{response.text}")

# Analyze technology sector
asyncio.run(sector_analysis("technology"))
```

## Step 8: Technical Analysis

```python
async def technical_analysis(symbol: str):
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Perform technical analysis on {symbol}:
    1. Calculate RSI (Relative Strength Index)
    2. Identify support and resistance levels
    3. Check MACD indicator
    4. Analyze volume trends
    5. Provide buy/sell/hold recommendation based on technicals
    """

    response = await analyst.chat(query)
    print(f"\nTechnical Analysis for {symbol}:")
    print(response.text)

asyncio.run(technical_analysis("TSLA"))
```

## Step 9: News Sentiment Analysis

```python
async def news_sentiment(symbol: str):
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Analyze recent news sentiment for {symbol}:
    1. Summarize top 5 recent news articles
    2. Classify sentiment (positive/negative/neutral)
    3. Identify key themes
    4. Assess potential impact on stock price
    """

    response = await analyst.chat(query)
    print(f"\nNews Sentiment for {symbol}:")
    print(response.text)

asyncio.run(news_sentiment("NVDA"))
```

## Step 10: Market Forecast

```python
async def market_forecast(symbol: str, timeframe: str = "next quarter"):
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Provide a price forecast for {symbol} for {timeframe}:
    1. Current price
    2. Historical price trends
    3. Key factors affecting future price
    4. Optimistic scenario price target
    5. Pessimistic scenario price target
    6. Most likely price target
    7. Confidence level in forecast
    """

    response = await analyst.chat(query)
    print(f"\nForecast for {symbol} ({timeframe}):")
    print(response.text)

asyncio.run(market_forecast("AAPL", "next quarter"))
```

## Step 11: Batch Analysis

```python
async def batch_analysis(symbols: list):
    """Analyze multiple stocks sequentially."""
    analyst = SingleAssistant("Market_Analyst")

    results = []
    for symbol in symbols:
        # Reset context for each stock
        analyst.reset()

        response = await analyst.chat(
            f"Provide a brief analysis of {symbol}: "
            f"current price, day change, and outlook."
        )

        results.append({
            'symbol': symbol,
            'analysis': response.text
        })

    # Print results
    print("\n" + "="*60)
    print("BATCH ANALYSIS RESULTS")
    print("="*60)

    for result in results:
        print(f"\n{result['symbol']}:")
        print(result['analysis'])
        print("-"*60)

asyncio.run(batch_analysis(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]))
```

## Step 12: Error Handling

```python
async def robust_analysis(symbol: str):
    """Analysis with error handling."""
    analyst = SingleAssistant("Market_Analyst")

    try:
        response = await analyst.chat(
            f"Analyze {symbol} stock"
        )
        print(f"✓ Analysis successful:")
        print(response.text)

    except Exception as e:
        print(f"✗ Error analyzing {symbol}: {e}")

        # Fallback to simpler query
        try:
            response = await analyst.chat(
                f"What is {symbol} current stock price?"
            )
            print(f"✓ Fallback query successful:")
            print(response.text)
        except Exception as e2:
            print(f"✗ Fallback also failed: {e2}")

# Test with valid symbol
asyncio.run(robust_analysis("AAPL"))

# Test with invalid symbol
asyncio.run(robust_analysis("INVALID"))
```

## Step 13: Save Results

```python
async def analyze_and_save(symbol: str, filename: str = None):
    """Analyze stock and save results to file."""
    analyst = SingleAssistant("Market_Analyst")

    query = f"""
    Comprehensive analysis of {symbol}:
    - Current price and change
    - Technical indicators
    - Recent news
    - Forecast
    """

    response = await analyst.chat(query)

    # Save to file
    if filename is None:
        filename = f"{symbol}_analysis.txt"

    with open(filename, "w") as f:
        f.write(f"Analysis for {symbol}\n")
        f.write("="*60 + "\n\n")
        f.write(response.text)
        f.write("\n\n" + "="*60 + "\n")

    print(f"✓ Analysis saved to {filename}")
    return response.text

asyncio.run(analyze_and_save("NVDA", "nvda_analysis.txt"))
```

## Complete Example: Market Dashboard

```python
async def market_dashboard(watchlist: list):
    """Create a market dashboard for watchlist."""
    analyst = SingleAssistant("Market_Analyst")

    print("\n" + "="*60)
    print("MARKET DASHBOARD")
    print("="*60 + "\n")

    for symbol in watchlist:
        analyst.reset()  # Fresh context for each stock

        response = await analyst.chat(
            f"Quick summary for {symbol}: price, change%, and 1-line outlook"
        )

        print(f"{symbol}: {response.text}")
        print()

    # Market overview
    analyst.reset()
    overview = await analyst.chat(
        "Provide a 2-sentence overall market sentiment for today"
    )

    print("="*60)
    print(f"Market Overview: {overview.text}")
    print("="*60)

# Run dashboard
watchlist = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
asyncio.run(market_dashboard(watchlist))
```

## Best Practices

### 1. Reset Context When Needed
```python
# Between unrelated queries
analyst.reset()
```

### 2. Be Specific in Queries
```python
# Good
"Get Apple (AAPL) price, 50-day MA, and RSI"

# Less effective
"Tell me about Apple"
```

### 3. Use Multi-turn for Related Queries
```python
# Related queries - keep context
await analyst.chat("Get NVDA price")
await analyst.chat("What was the change from yesterday?")  # Uses context
```

### 4. Handle Errors Gracefully
```python
try:
    response = await analyst.chat(query)
except Exception as e:
    print(f"Error: {e}")
```

## Exercises

Try these exercises to practice:

1. **Exercise 1**: Analyze your personal watchlist of 5 stocks
2. **Exercise 2**: Compare tech stocks vs energy stocks
3. **Exercise 3**: Create weekly summary report for a stock
4. **Exercise 4**: Build alert system for price changes
5. **Exercise 5**: Analyze correlation between related stocks

## Next Steps

- **[Tutorial 2: Investment Reports](02-investment-reports.md)** - Generate comprehensive reports
- **[Tutorial 3: Multi-Agent Collaboration](03-multi-agent-collaboration.md)** - Use multiple agents
- **[Workflows Guide](../user-guide/workflows.md)** - Learn more patterns
- **[Data Sources](../user-guide/data-sources.md)** - Understand data APIs

## Troubleshooting

**Issue**: Agent returns "Unable to get price"
- **Solution**: Check API keys are configured (FinnHub, FMP)

**Issue**: AsyncIO errors
- **Solution**: Ensure using `asyncio.run()` and `await`

**Issue**: Context not maintained
- **Solution**: Don't call `reset()` between related queries

## Summary

You learned to:
- ✓ Create Market Analyst agent
- ✓ Query stock prices and data
- ✓ Perform technical analysis
- ✓ Analyze news sentiment
- ✓ Generate forecasts
- ✓ Handle multiple stocks
- ✓ Save analysis results

Continue to Tutorial 2 to learn about generating investment reports!
