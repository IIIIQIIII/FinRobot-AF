# FinRobot - Agent Framework Edition

> Multi-Agent Framework for Financial Analysis
> Migrated from AutoGen to Microsoft Agent Framework

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Agent Framework](https://img.shields.io/badge/Agent%20Framework-2.0-green.svg)](https://github.com/microsoft/agent-framework)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

FinRobot is a sophisticated multi-agent framework for financial analysis, market forecasting, and automated report generation. This version has been migrated from AutoGen to Microsoft's Agent Framework, providing:

- **Modern Architecture**: Built on Agent Framework's stateless agents and workflow graphs
- **Enhanced Observability**: Integrated OpenTelemetry support
- **Flexible Orchestration**: Builder-pattern workflows for complex multi-agent coordination
- **Production Ready**: Improved state management and error handling

## Key Features

### Pre-configured Financial Agents

- **Market_Analyst**: Real-time market data analysis and forecasting
- **Expert_Investor**: Comprehensive financial report generation
- **Data_Analyst**: Python-based data analysis
- **Statistician**: Statistical modeling and analysis
- **Financial_Analyst**: Financial metrics and performance analysis

### Workflow Patterns

1. **SingleAssistant**: Basic agent-user interaction
2. **SingleAssistantRAG**: Retrieval-augmented generation for document analysis
3. **SingleAssistantShadow**: Dual-agent planning and execution
4. **MultiAssistant**: Group chat with multiple specialized agents
5. **MultiAssistantWithLeader**: Hierarchical multi-agent coordination

### Data Sources

- FinnHub: Company profiles, news, financials
- Yahoo Finance: Stock data, historical prices
- SEC: Official company filings
- Reddit: Sentiment analysis
- Financial Modeling Prep: Advanced financial data

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (or compatible LLM provider)
- Optional: API keys for data sources (FinnHub, SEC, FMP)

### Quick Start with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. It's significantly faster than pip and conda.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/IIIIQIIII/FinRobot-AF.git
cd FinRobot-AF

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package with all dependencies
uv pip install --pre -e .

# Optional: Install development dependencies
uv pip install --pre -e ".[dev]"

# Optional: Install Jupyter support
uv pip install --pre -e ".[jupyter]"
```

### Alternative: Installation with conda

If you prefer conda for environment management:

**Quick install (using script):**
```bash
# Linux/macOS
./scripts/install_conda.sh

# Windows
scripts\install_conda.bat
```

**Manual install:**
```bash
# Create conda environment
conda create -n finrobot python=3.10 -y
conda activate finrobot

# Install dependencies (note: --pre flag required for agent-framework)
pip install --pre -r requirements.txt

# Install FinRobot package
pip install -e .
```

**Important**: The `--pre` flag is required for installing `agent-framework-core` (pre-release).

See [docs/installation.md](docs/installation.md) for detailed installation instructions and troubleshooting.

### Configuration

Create configuration files in your working directory:

**1. OAI_CONFIG_LIST** (LLM Configuration)
```json
[
    {
        "model": "gpt-4",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1"
    }
]
```

**2. config_api_keys** (Data Source API Keys)
```json
{
    "FINNHUB_API_KEY": "your_finnhub_key",
    "FMP_API_KEY": "your_fmp_key",
    "SEC_API_KEY": "your_sec_key",
    "OPENAI_API_KEY": "sk-..."
}
```

## Quick Start

### Example 1: Market Analysis

```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

# Initialize configuration
config = initialize_config(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)

# Create market analyst
assistant = SingleAssistant("Market_Analyst")

# Analyze stock
async def analyze_stock():
    response = await assistant.chat(
        "Analyze NVDA stock performance and provide forecast for next quarter"
    )
    print(response.text)

asyncio.run(analyze_stock())
```

### Example 2: Financial Report Generation

```python
from finrobot.agents.workflows import SingleAssistantShadow

# Create expert investor with planning capability
assistant = SingleAssistantShadow("Expert_Investor")

# Generate comprehensive report
async def generate_report():
    response = await assistant.chat(
        "Create a detailed investment analysis report for Microsoft (MSFT) "
        "including financial statements, market position, and investment recommendation"
    )
    print(response.text)

asyncio.run(generate_report())
```

### Example 3: Multi-Agent Collaboration

```python
from finrobot.agents.workflows import MultiAssistant

# Create multi-agent team
team = MultiAssistant([
    "Market_Analyst",
    "Financial_Analyst",
    "Statistician"
])

# Collaborative analysis
async def team_analysis():
    response = await team.chat(
        "Perform comprehensive analysis of Tesla (TSLA) stock: "
        "market trends, financial health, and statistical risk assessment"
    )
    print(response.text)

asyncio.run(team_analysis())
```

### Example 4: RAG-Enhanced Analysis

```python
from finrobot.agents.workflows import SingleAssistantRAG

# Create RAG-enabled assistant
assistant = SingleAssistantRAG(
    "Expert_Investor",
    docs_path="./financial_reports",
    collection_name="earnings_reports"
)

# Query with document context
async def rag_query():
    response = await assistant.chat(
        "Based on recent earnings reports, what are the key risks for tech sector?"
    )
    print(response.text)

asyncio.run(rag_query())
```

## Migration from AutoGen

If you're migrating existing FinRobot AutoGen code, see [MIGRATION_PLAN.md](MIGRATION_PLAN.md) for detailed guidance.

### Key Differences

| Aspect | AutoGen | Agent Framework |
|--------|---------|-----------------|
| State Management | Implicit | Explicit (AgentThread) |
| Tool Execution | Single-turn default | Multi-turn default |
| Orchestration | GroupChat classes | Builder patterns |
| Response Handling | Synchronous | Async/await |

### Quick Migration Example

**Before (AutoGen):**
```python
from finrobot.agents.workflow import SingleAssistant

assistant = SingleAssistant("Market_Analyst", llm_config)
assistant.chat("Analyze NVDA stock")
```

**After (Agent Framework):**
```python
from finrobot.agents.workflows import SingleAssistant

assistant = SingleAssistant("Market_Analyst")
response = await assistant.chat("Analyze NVDA stock")
print(response.text)
```

## Architecture

```
finrobot-af/
├── finrobot/
│   ├── agents/
│   │   ├── agent_library.py    # Pre-configured agent definitions
│   │   ├── workflows.py         # Workflow orchestration patterns
│   │   ├── prompts.py           # System prompts
│   │   └── __init__.py
│   ├── data_source/             # Financial data integrations
│   │   ├── finnhub_utils.py
│   │   ├── yfinance_utils.py
│   │   ├── sec_utils.py
│   │   └── ...
│   ├── functional/              # Specialized capabilities
│   │   ├── analyzer.py          # Financial analysis
│   │   ├── charting.py          # Visualization
│   │   ├── coding.py            # Code generation
│   │   ├── rag.py               # RAG utilities
│   │   └── ...
│   ├── config.py                # Configuration management
│   ├── toolkits.py              # Tool registration
│   └── utils.py                 # Helper functions
├── docs/                        # Documentation
│   ├── tutorials/               # Tutorial documentation
│   └── ...
├── examples/                    # Usage examples
└── tests/                       # Test suite
```

## Available Agents

### General Purpose
- `Software_Developer`: Python programming
- `Data_Analyst`: Data analysis
- `Programmer`: General programming
- `IT_Specialist`: Technical problem-solving

### Financial Specialists
- `Market_Analyst`: Market data collection and forecasting
- `Expert_Investor`: Investment analysis and reporting
- `Financial_Analyst`: Financial metrics analysis
- `Accountant`: Accounting principles and analysis
- `Statistician`: Statistical modeling

### AI/ML
- `Artificial_Intelligence_Engineer`: AI/ML tasks

## Workflow Patterns

### 1. SingleAssistant
Basic agent interaction with tool execution.

```python
assistant = SingleAssistant("Market_Analyst")
response = await assistant.chat("Get AAPL stock price")
```

### 2. SingleAssistantRAG
Agent with document retrieval.

```python
assistant = SingleAssistantRAG(
    "Expert_Investor",
    docs_path="./docs"
)
response = await assistant.chat("Analyze Q3 earnings")
```

### 3. SingleAssistantShadow
Dual-agent planning and execution.

```python
assistant = SingleAssistantShadow("Expert_Investor")
response = await assistant.chat("Create comprehensive report")
```

### 4. MultiAssistant
Group chat with multiple agents.

```python
team = MultiAssistant([
    "Market_Analyst",
    "Financial_Analyst"
])
response = await team.chat("Analyze market trends")
```

### 5. MultiAssistantWithLeader
Hierarchical coordination.

```python
workflow = MultiAssistantWithLeader(
    leader_config="Financial_Analyst",
    team_configs=["Data_Analyst", "Statistician"]
)
response = await workflow.chat("Complete financial analysis")
```

## Advanced Usage

### Custom Agent Configuration

```python
from finrobot.agents.agent_library import create_agent
from finrobot.config import get_config

config = get_config()
client = config.get_chat_client()

custom_agent = create_agent(
    {
        "name": "Custom_Analyst",
        "description": "Custom financial analyst",
        "instructions": "You are a specialized analyst...",
        "toolkits": ["market_data", "charting"]
    },
    chat_client=client
)
```

### Streaming Responses

```python
assistant = SingleAssistant("Market_Analyst")

async for chunk in assistant.chat("Analyze TSLA", stream=True):
    print(chunk.text, end="", flush=True)
```

### Custom Tools

```python
from typing import Annotated
from pydantic import Field

def get_custom_metric(
    symbol: Annotated[str, Field(description="Stock symbol")]
) -> str:
    """Calculate custom financial metric."""
    # Your implementation
    return f"Custom metric for {symbol}"

# Register with agent
from finrobot.toolkits import create_tool_from_function

tool = create_tool_from_function(get_custom_metric)
# Add to agent's tools list
```

## Testing

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_workflows.py

# Run with coverage
pytest --cov=finrobot tests/
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure Agent Framework is installed: `pip install agent-framework`
   - Check Python version: `python --version` (must be 3.10+)

2. **API Key Errors**
   - Verify config files exist: `OAI_CONFIG_LIST`, `config_api_keys`
   - Check environment variables: `echo $OPENAI_API_KEY`

3. **AsyncIO Errors**
   - Use `asyncio.run()` for top-level async calls
   - Ensure all workflow methods are awaited

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- **Original FinRobot**: [AI4Finance-Foundation/FinRobot](https://github.com/AI4Finance-Foundation/FinRobot)
- **Agent Framework**: [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- **AutoGen**: [Microsoft AutoGen](https://github.com/microsoft/autogen)

## Citation

If you use FinRobot in your research, please cite:

```bibtex
@software{finrobot_af_2024,
  title={FinRobot: Multi-Agent Framework for Financial Analysis (Agent Framework Edition)},
  author={AI4Finance Foundation},
  year={2024},
  url={https://github.com/AI4Finance-Foundation/FinRobot}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/IIIIQIIII/FinRobot-AF/issues)
- **Discussions**: [GitHub Discussions](https://github.com/IIIIQIIII/FinRobot-AF/discussions)
- **Documentation**: [Full Documentation](docs/README.md)

---

**Built with** ❤️ **by AI4Finance Foundation | Powered by Microsoft Agent Framework**
