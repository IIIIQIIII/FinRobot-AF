# Agents User Guide

Learn about FinRobot's agent system and how to use pre-configured financial agents effectively.

## Understanding Agents

In FinRobot-AF, agents are AI-powered assistants specialized for financial analysis tasks. Each agent:

- Has specific **instructions** defining its role and behavior
- Can use **tools** to access data and perform operations
- Maintains **conversation state** through threads
- Operates **asynchronously** for efficient execution

## Agent Architecture

```
Agent = Instructions + Tools + Chat Client + Thread
```

- **Instructions**: System prompt defining agent's role and capabilities
- **Tools**: Functions the agent can call (data APIs, analysis functions)
- **Chat Client**: LLM provider (OpenAI, Azure OpenAI, etc.)
- **Thread**: Conversation history and state management

## Pre-configured Agents

### Financial Specialists

#### Market_Analyst
**Specialty**: Real-time market data and forecasting

```python
from finrobot.agents.workflows import SingleAssistant

analyst = SingleAssistant("Market_Analyst")
response = await analyst.chat(
    "Analyze Apple (AAPL) stock performance and forecast next quarter"
)
```

**Available Tools**:
- Stock price retrieval (real-time & historical)
- Company profiles
- Market news
- Technical indicators
- Price forecasting

**Best For**:
- Stock price queries
- Market trend analysis
- Technical analysis
- Price forecasting
- News sentiment

#### Expert_Investor
**Specialty**: Comprehensive investment analysis and reporting

```python
from finrobot.agents.workflows import SingleAssistantShadow

investor = SingleAssistantShadow("Expert_Investor")
response = await investor.chat(
    "Create an investment report for Microsoft including fundamentals and recommendation"
)
```

**Available Tools**:
- All Market_Analyst tools
- Financial statement analysis
- Investment metrics
- Report generation
- PDF creation

**Best For**:
- Investment reports
- Stock recommendations
- Comprehensive analysis
- Portfolio evaluation

#### Financial_Analyst
**Specialty**: Financial metrics and statement analysis

```python
analyst = SingleAssistant("Financial_Analyst")
response = await analyst.chat(
    "Analyze Tesla's balance sheet and calculate key financial ratios"
)
```

**Available Tools**:
- Financial statements (10-K, 10-Q)
- Ratio calculations
- Trend analysis
- Comparative analysis

**Best For**:
- Financial statement analysis
- Ratio calculations
- Profitability analysis
- Financial health assessment

#### Statistician
**Specialty**: Statistical modeling and quantitative analysis

```python
statistician = SingleAssistant("Statistician")
response = await statistician.chat(
    "Perform statistical analysis on NVDA returns and calculate risk metrics"
)
```

**Available Tools**:
- Statistical tests
- Risk calculations
- Correlation analysis
- Distribution fitting

**Best For**:
- Risk analysis
- Statistical testing
- Correlation studies
- Quantitative modeling

### General Purpose Agents

#### Data_Analyst
**Specialty**: Python-based data analysis

```python
analyst = SingleAssistant("Data_Analyst")
response = await analyst.chat(
    "Load and analyze the quarterly earnings data from the CSV file"
)
```

**Best For**:
- Data processing
- Custom calculations
- File analysis
- Data visualization

#### Software_Developer
**Specialty**: Python programming and code generation

```python
developer = SingleAssistant("Software_Developer")
response = await developer.chat(
    "Write a function to calculate moving average convergence divergence (MACD)"
)
```

**Best For**:
- Custom tool development
- Code generation
- Algorithm implementation
- Debugging

## Creating Agents

### Using Pre-configured Agents

The simplest way to create an agent:

```python
from finrobot.agents.workflows import SingleAssistant

# By name
agent = SingleAssistant("Market_Analyst")

# Use the agent
response = await agent.chat("What is AAPL stock price?")
print(response.text)
```

### Custom Agent Configuration

Create agents with custom settings:

```python
from finrobot.agents.agent_library import create_agent
from finrobot.config import get_config

config = get_config()
client = config.get_chat_client()

# Custom agent
custom_agent = create_agent(
    {
        "name": "Custom_Analyst",
        "description": "Specialized crypto analyst",
        "instructions": """
            You are a cryptocurrency market analyst.
            You provide analysis on crypto markets and blockchain technology.
            Reply 'TERMINATE' when the task is complete.
        """,
        "toolkits": ["market_data", "charting"]
    },
    chat_client=client
)
```

### Modifying Existing Agents

Override default configuration:

```python
from finrobot.agents.agent_library import AGENT_CONFIGS, create_agent
from finrobot.config import get_config

# Get base config
config_dict = AGENT_CONFIGS["Market_Analyst"].copy()

# Modify instructions
config_dict["instructions"] = """
    You are a market analyst focused on tech stocks.
    Provide detailed analysis with emphasis on technology sector.
    Reply 'TERMINATE' when complete.
"""

# Add additional tools
config_dict["toolkits"].append("custom_tech_analysis")

# Create modified agent
client = get_config().get_chat_client()
agent = create_agent(config_dict, chat_client=client)
```

## Agent Interactions

### Basic Chat

```python
# Single turn
response = await agent.chat("Get AAPL stock price")
print(response.text)
```

### Multi-turn Conversations

Agents maintain conversation history through threads:

```python
# First turn
response1 = await agent.chat("Get AAPL current price")
print(response1.text)

# Second turn (context from first turn available)
response2 = await agent.chat("What was the price change from yesterday?")
print(response2.text)

# Third turn
response3 = await agent.chat("Based on this, what's your forecast?")
print(response3.text)
```

### Resetting Agent State

```python
# Reset conversation history
agent.reset()

# Now starts fresh conversation
response = await agent.chat("Get MSFT stock price")
```

### Streaming Responses

Get responses as they're generated:

```python
# Stream response chunks
async for chunk in agent.chat("Analyze TSLA stock", stream=True):
    print(chunk.text, end="", flush=True)
```

## Agent Configuration Options

### Max Turns

Control maximum conversation rounds:

```python
agent = SingleAssistant(
    "Market_Analyst",
    max_turns=20  # Default is 10
)
```

### Custom Chat Client

Use different LLM provider:

```python
from agent_framework.openai import OpenAIChatClient

# Custom client with specific model
client = OpenAIChatClient(
    model_id="gpt-4-turbo",
    api_key="sk-...",
    temperature=0.7
)

agent = SingleAssistant(
    "Market_Analyst",
    chat_client=client
)
```

### Custom Toolkit Registry

Provide custom tools:

```python
from finrobot.toolkits import create_default_toolkit_registry
from typing import Annotated
from pydantic import Field

# Create custom tool
def get_crypto_price(symbol: Annotated[str, Field(description="Crypto symbol")]) -> str:
    """Get cryptocurrency price."""
    # Implementation
    return f"Price for {symbol}: $50000"

# Create registry with custom tool
registry = create_default_toolkit_registry()
registry["crypto_tools"] = [get_crypto_price]

# Create agent with custom registry
agent = SingleAssistant(
    "Market_Analyst",
    toolkit_registry=registry
)
```

## Best Practices

### 1. Choose the Right Agent

Match agent to task:
- **Quick price queries** → Market_Analyst
- **Comprehensive reports** → Expert_Investor (with Shadow workflow)
- **Financial statement analysis** → Financial_Analyst
- **Risk analysis** → Statistician
- **Data processing** → Data_Analyst

### 2. Provide Clear Instructions

```python
# Good: Specific and clear
response = await agent.chat(
    "Get Apple (AAPL) stock price, calculate 50-day moving average, "
    "and compare to current price"
)

# Less effective: Vague
response = await agent.chat("Tell me about Apple")
```

### 3. Use Multi-turn for Complex Tasks

```python
# Break complex tasks into steps
response1 = await agent.chat("Get financial statements for TSLA")
response2 = await agent.chat("Calculate profit margin trend over last 4 quarters")
response3 = await agent.chat("Compare with industry average")
```

### 4. Reset State When Needed

```python
# Analyze first stock
await agent.chat("Analyze AAPL")
await agent.chat("What's the forecast?")

# Reset before analyzing different stock
agent.reset()

# Analyze second stock (fresh context)
await agent.chat("Analyze MSFT")
```

### 5. Handle Errors Gracefully

```python
try:
    response = await agent.chat("Get stock price for INVALID_SYMBOL")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
```

## Advanced Agent Features

### Agent with RAG

Combine agents with document retrieval:

```python
from finrobot.agents.workflows import SingleAssistantRAG

# Agent with access to document collection
rag_agent = SingleAssistantRAG(
    "Expert_Investor",
    docs_path="./financial_reports",
    collection_name="earnings_reports"
)

# Query with document context
response = await rag_agent.chat(
    "Based on recent earnings reports, analyze tech sector trends"
)
```

### Planning Agent (Shadow Pattern)

Use dual-agent planning:

```python
from finrobot.agents.workflows import SingleAssistantShadow

# Planner + Executor pattern
shadow_agent = SingleAssistantShadow("Expert_Investor")

# Agent creates plan then executes
response = await shadow_agent.chat(
    "Create comprehensive investment analysis for NVDA: "
    "fundamentals, technicals, valuation, and recommendation"
)
```

### Custom Termination Conditions

Control when agent stops:

```python
# Implement custom termination logic
class CustomAssistant(SingleAssistant):
    async def chat(self, message: str, **kwargs):
        response = await super().chat(message, **kwargs)

        # Custom termination check
        if "TERMINATE" in response.text or len(response.text) > 5000:
            print("Terminating conversation")
            return response

        return response
```

## Debugging Agents

### Enable Verbose Output

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Now see detailed agent operations
response = await agent.chat("Analyze AAPL")
```

### Inspect Thread State

```python
# Access conversation history
thread = agent.thread
messages = thread.messages

# Print conversation
for msg in messages:
    print(f"{msg.role}: {msg.text}")
```

### Monitor Tool Calls

```python
# Check which tools were called
response = await agent.chat("Get AAPL price and news")

# Inspect tool calls in response
if hasattr(response, 'tool_calls'):
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call.name}")
        print(f"Args: {tool_call.arguments}")
```

## Next Steps

- **[Workflows Guide](workflows.md)** - Learn about workflow orchestration
- **[Tools Guide](tools.md)** - Understand available tools
- **[Tutorials](../tutorials/04-custom-agents.md)** - Build custom agents
- **[API Reference](../api/agents.md)** - Detailed API documentation
