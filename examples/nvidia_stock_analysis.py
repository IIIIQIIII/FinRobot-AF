#!/usr/bin/env python
"""
NVIDIA Stock Analysis Example

This example demonstrates direct usage of yfinance utilities to:
1. Fetch NVIDIA stock data using yfinance
2. Perform basic stock analysis
3. Generate and save analysis report to results/reports/

Usage:
    python examples/nvidia_stock_analysis.py
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from finrobot.data_source.yfinance_utils import YFinanceUtils


def analyze_nvidia_stock():
    """
    Analyze NVIDIA stock using yfinance utilities directly.

    This simplified version:
    - Fetches current stock info
    - Gets historical stock data
    - Retrieves financial statements
    - Generates basic analysis report
    """

    print("="*80)
    print("NVIDIA STOCK ANALYSIS (Simplified)")
    print("="*80)
    print()

    symbol = "NVDA"

    # Define analysis timeframe
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last 1 year

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    print(f"Analyzing {symbol} from {start_str} to {end_str}")
    print()

    # Step 1: Get current stock info
    print("Step 1: Fetching current stock information...")
    try:
        stock_info = YFinanceUtils.get_stock_info(symbol)
        current_price = stock_info.get('currentPrice', 'N/A')
        market_cap = stock_info.get('marketCap', 'N/A')
        pe_ratio = stock_info.get('trailingPE', 'N/A')
        week_52_high = stock_info.get('fiftyTwoWeekHigh', 'N/A')
        week_52_low = stock_info.get('fiftyTwoWeekLow', 'N/A')

        print(f"✅ Current Price: ${current_price}")
        print(f"   Market Cap: ${market_cap:,}" if isinstance(market_cap, (int, float)) else f"   Market Cap: {market_cap}")
        print(f"   P/E Ratio: {pe_ratio}")
        print(f"   52-Week High: ${week_52_high}")
        print(f"   52-Week Low: ${week_52_low}")
        print()
    except Exception as e:
        print(f"❌ Error fetching stock info: {e}")
        return False

    # Step 2: Get historical stock data
    print("Step 2: Fetching historical stock data...")
    try:
        stock_data = YFinanceUtils.get_stock_data(symbol, start_str, end_str)
        print(f"✅ Retrieved {len(stock_data)} days of historical data")
        print()
    except Exception as e:
        print(f"❌ Error fetching stock data: {e}")
        return False

    # Step 3: Get company information
    print("Step 3: Fetching company information...")
    try:
        company_info = YFinanceUtils.get_company_info(symbol)
        print(f"✅ Company: {company_info.iloc[0]['Company Name']}")
        print(f"   Sector: {company_info.iloc[0]['Sector']}")
        print(f"   Industry: {company_info.iloc[0]['Industry']}")
        print()
    except Exception as e:
        print(f"❌ Error fetching company info: {e}")
        return False

    # Step 4: Get financial statements
    print("Step 4: Fetching financial statements...")
    try:
        income_stmt = YFinanceUtils.get_income_stmt(symbol)
        balance_sheet = YFinanceUtils.get_balance_sheet(symbol)
        cash_flow = YFinanceUtils.get_cash_flow(symbol)
        print(f"✅ Income Statement: {income_stmt.shape[1]} periods")
        print(f"✅ Balance Sheet: {balance_sheet.shape[1]} periods")
        print(f"✅ Cash Flow: {cash_flow.shape[1]} periods")
        print()
    except Exception as e:
        print(f"❌ Error fetching financial statements: {e}")
        return False

    # Step 5: Generate and save report
    print("Step 5: Generating analysis report...")
    try:
        # Create reports directory
        reports_dir = Path("results/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"NVIDIA_Stock_Analysis_{timestamp}.md"
        report_path = reports_dir / report_filename

        # Calculate some basic metrics
        price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]
        price_change_pct = (price_change / stock_data['Close'].iloc[0]) * 100
        avg_volume = stock_data['Volume'].mean()
        volatility = stock_data['Close'].std()

        # Create report content
        report_content = f"""# NVIDIA Corporation (NVDA) Stock Analysis Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Analysis Period**: {start_str} to {end_str}
**Data Source**: Yahoo Finance (yfinance)

---

## Executive Summary

This report provides a comprehensive analysis of NVIDIA Corporation (NVDA) stock performance
and financial health over the past 12 months.

## 1. Current Stock Information

- **Current Price**: ${current_price}
- **Market Capitalization**: ${market_cap:,}
- **P/E Ratio**: {pe_ratio}
- **52-Week High**: ${week_52_high}
- **52-Week Low**: ${week_52_low}

## 2. Company Overview

- **Company Name**: {company_info.iloc[0]['Company Name']}
- **Sector**: {company_info.iloc[0]['Sector']}
- **Industry**: {company_info.iloc[0]['Industry']}
- **Country**: {company_info.iloc[0]['Country']}
- **Website**: {company_info.iloc[0]['Website']}

## 3. Historical Performance (Past Year)

### Price Performance
- **Starting Price** (12 months ago): ${stock_data['Close'].iloc[0]:.2f}
- **Ending Price** (current): ${stock_data['Close'].iloc[-1]:.2f}
- **Change**: ${price_change:.2f} ({price_change_pct:+.2f}%)
- **Highest Price**: ${stock_data['High'].max():.2f}
- **Lowest Price**: ${stock_data['Low'].min():.2f}

### Trading Metrics
- **Average Daily Volume**: {avg_volume:,.0f} shares
- **Price Volatility (Std Dev)**: ${volatility:.2f}

## 4. Financial Statements Summary

### Income Statement
Available periods: {income_stmt.shape[1]}
Key metrics available: {', '.join(list(income_stmt.index[:5]))}

### Balance Sheet
Available periods: {balance_sheet.shape[1]}
Key metrics available: {', '.join(list(balance_sheet.index[:5]))}

### Cash Flow Statement
Available periods: {cash_flow.shape[1]}
Key metrics available: {', '.join(list(cash_flow.index[:5]))}

## 5. Analysis Summary

### Stock Performance
{"📈 Strong performance" if price_change_pct > 0 else "📉 Negative performance"} over the past year with a {"gain" if price_change_pct > 0 else "loss"} of {abs(price_change_pct):.2f}%.

### Volatility Assessment
The stock showed {"high" if volatility > 10 else "moderate" if volatility > 5 else "low"} volatility with a standard deviation of ${volatility:.2f}.

### Trading Activity
Average daily trading volume of {avg_volume:,.0f} shares indicates {"high" if avg_volume > 50000000 else "moderate" if avg_volume > 10000000 else "low"} liquidity.

---

## Data Summary

### Historical Stock Data Preview
{stock_data.tail(5).to_string()}

---

*This report was generated automatically by FinRobot-AF using yfinance utilities.*
*Data source: Yahoo Finance*
*Note: This is a simplified analysis. For investment decisions, consult a financial advisor.*
"""

        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✅ Report saved to: {report_path}")
        print()

        print("="*80)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*80)
        print()
        print(f"📄 Full report: {report_path}")
        print()

        return True

    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return False


def quick_nvidia_info():
    """
    Quick example: Just get current NVIDIA stock info.
    """

    print("="*80)
    print("NVIDIA QUICK INFO")
    print("="*80)
    print()

    symbol = "NVDA"

    try:
        stock_info = YFinanceUtils.get_stock_info(symbol)
        company_info = YFinanceUtils.get_company_info(symbol)

        print(f"Company: {company_info.iloc[0]['Company Name']}")
        print(f"Sector: {company_info.iloc[0]['Sector']}")
        print(f"Industry: {company_info.iloc[0]['Industry']}")
        print()
        print(f"Current Price: ${stock_info.get('currentPrice', 'N/A')}")
        print(f"Market Cap: ${stock_info.get('marketCap', 'N/A'):,}" if isinstance(stock_info.get('marketCap'), (int, float)) else f"Market Cap: {stock_info.get('marketCap', 'N/A')}")
        print(f"P/E Ratio: {stock_info.get('trailingPE', 'N/A')}")
        print(f"52-Week High: ${stock_info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52-Week Low: ${stock_info.get('fiftyTwoWeekLow', 'N/A')}")
        print()

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to run the stock analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Analyze NVIDIA stock using yfinance utilities'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick info check instead of full analysis'
    )

    args = parser.parse_args()

    if args.quick:
        success = quick_nvidia_info()
    else:
        success = analyze_nvidia_stock()

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
