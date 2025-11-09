# Quick Start Guide

Get started with FinRobot-AF in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (or compatible LLM provider)
- Basic understanding of async/await in Python

## Installation

### 1. Install FinRobot-AF

```bash
# Create and activate conda environment
conda create -n finrobot python=3.10
conda activate finrobot

# Clone repository (or install from PyPI when available)
git clone https://github.com/AI4Finance-Foundation/FinRobot-AF.git
cd FinRobot-AF

# Install dependencies
pip install -r requirements.txt

# Install FinRobot package
pip install -e .
```

### 2. Setup Configuration Files

Create two configuration files in your working directory:

**OAI_CONFIG_LIST** (LLM Configuration):
```json
[
    {
        "model": "gpt-4",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1"
    }
]
```

**config_api_keys** (Optional - for data sources):
```json
{
    "OPENAI_API_KEY": "sk-...",
    "FINNHUB_API_KEY": "your_finnhub_key",
    "FMP_API_KEY": "your_fmp_key"
}
```

## Your First Agent

### Example 1: Simple Market Query

Create a file `first_agent.py`:

```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

async def main():
    # Initialize configuration
    config = initialize_config(
        api_keys_path="config_api_keys",
        llm_config_path="OAI_CONFIG_LIST"
    )

    # Create a market analyst agent
    assistant = SingleAssistant("Market_Analyst")

    # Ask a question
    response = await assistant.chat(
        "What is the current stock price of Apple (AAPL)?"
    )

    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python first_agent.py
```

### Example 2: Stock Analysis

```python
import asyncio
from finrobot.agents.workflows import SingleAssistant

async def analyze_stock():
    # Create analyst
    assistant = SingleAssistant("Market_Analyst")

    # Perform analysis
    response = await assistant.chat(
        "Analyze NVIDIA (NVDA) stock performance over the last quarter "
        "and provide a short-term forecast."
    )

    print(response.text)

asyncio.run(analyze_stock())
```

### Example 3: Financial Report Generation

```python
import asyncio
from finrobot.agents.workflows import SingleAssistantShadow

async def generate_report():
    # Create expert investor with planning capability
    assistant = SingleAssistantShadow("Expert_Investor")

    # Generate comprehensive report
    response = await assistant.chat(
        "Create a brief investment analysis report for Microsoft (MSFT) "
        "including current price, key metrics, and recommendation."
    )

    print(response.text)

asyncio.run(generate_report())
```

### Example 4: Multi-Agent Collaboration

```python
import asyncio
from finrobot.agents.workflows import MultiAssistant

async def team_analysis():
    # Create a team of specialized agents
    team = MultiAssistant([
        "Market_Analyst",
        "Financial_Analyst"
    ])

    # Collaborative analysis
    response = await team.chat(
        "Analyze Tesla (TSLA): market trends and financial health."
    )

    print(response.text)

asyncio.run(team_analysis())
```

## Available Agents

FinRobot-AF comes with pre-configured financial agents:

| Agent | Specialty | Use Case |
|-------|-----------|----------|
| `Market_Analyst` | Market data & forecasting | Stock analysis, market trends |
| `Expert_Investor` | Investment analysis | Investment reports, recommendations |
| `Financial_Analyst` | Financial metrics | Balance sheets, financial ratios |
| `Data_Analyst` | Data analysis | Python-based data processing |
| `Statistician` | Statistical modeling | Risk analysis, statistical tests |

## Workflow Patterns

FinRobot-AF provides 5 workflow patterns:

1. **SingleAssistant**: Basic agent-user interaction
   ```python
   assistant = SingleAssistant("Market_Analyst")
   ```

2. **SingleAssistantRAG**: Agent with document retrieval
   ```python
   assistant = SingleAssistantRAG("Expert_Investor", docs_path="./reports")
   ```

3. **SingleAssistantShadow**: Dual-agent planning and execution
   ```python
   assistant = SingleAssistantShadow("Expert_Investor")
   ```

4. **MultiAssistant**: Group chat with multiple agents
   ```python
   team = MultiAssistant(["Market_Analyst", "Financial_Analyst"])
   ```

5. **MultiAssistantWithLeader**: Hierarchical coordination
   ```python
   workflow = MultiAssistantWithLeader(
       leader_config="Financial_Analyst",
       team_configs=["Data_Analyst", "Statistician"]
   )
   ```

## Common Data Operations

### Get Stock Price
```python
assistant = SingleAssistant("Market_Analyst")
response = await assistant.chat("Get current price for AAPL")
```

### Get Company Profile
```python
response = await assistant.chat("Get company profile for Microsoft")
```

### Analyze Financial Statements
```python
assistant = SingleAssistant("Financial_Analyst")
response = await assistant.chat(
    "Analyze the balance sheet for Tesla (TSLA)"
)
```

## Next Steps

Now that you've created your first agent, explore:

- **[User Guide](user-guide/agents.md)** - Deep dive into agents and workflows
- **[Tutorials](tutorials/01-market-analysis.md)** - Step-by-step tutorials
- **[Data Sources](user-guide/data-sources.md)** - Learn about available data sources
- **[Custom Agents](tutorials/04-custom-agents.md)** - Create your own specialized agents

## Troubleshooting

### Common Issues

**Import Error: No module named 'agent_framework'**
```bash
pip install agent-framework --pre
```

**API Key Not Found**
- Verify `config_api_keys` file exists in working directory
- Check JSON format is valid
- Ensure OPENAI_API_KEY is set

**AsyncIO Error**
- Always use `asyncio.run()` for top-level async calls
- Ensure all workflow methods are awaited

For more help, see the [Troubleshooting Guide](reference/troubleshooting.md).
