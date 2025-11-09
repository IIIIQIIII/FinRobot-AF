# Frequently Asked Questions (FAQ)

Common questions and answers about FinRobot-AF.

## General Questions

### What is FinRobot-AF?

FinRobot-AF is a multi-agent framework for financial analysis built on Microsoft Agent Framework. It provides pre-configured financial agents, workflow orchestration patterns, and integrations with financial data sources.

### What's the difference from original FinRobot?

FinRobot-AF is migrated from AutoGen to Microsoft Agent Framework, providing:
- Modern async/await architecture
- Explicit state management via threads
- Builder-pattern workflows
- Enhanced observability
- Better production readiness

### Do I need programming experience?

Basic Python knowledge is required, especially understanding:
- Async/await syntax
- Function calls
- Exception handling
- JSON configuration

### Is it free to use?

FinRobot-AF code is open source (MIT license), but you'll need:
- OpenAI API key (pay-as-you-go)
- Optional: Data source API keys (some have free tiers)

## Installation & Setup

### What Python version is required?

Python 3.10 or higher is required.

### How do I install FinRobot-AF?

```bash
# Clone repository
git clone https://github.com/AI4Finance-Foundation/FinRobot-AF.git
cd FinRobot-AF

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### What API keys do I need?

**Required**:
- OpenAI API key

**Optional** (for data sources):
- FinnHub API key
- Financial Modeling Prep (FMP) API key
- SEC API key

### How do I get an OpenAI API key?

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Navigate to API Keys section
4. Create new secret key
5. Copy and save the key

### Can I use Azure OpenAI instead?

Yes! Configure in `OAI_CONFIG_LIST`:

```json
[
    {
        "model": "gpt-4",
        "api_key": "your-azure-key",
        "base_url": "https://your-resource.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    }
]
```

### Configuration files not found error?

Ensure config files are in your working directory:
```bash
ls OAI_CONFIG_LIST config_api_keys
```

Or provide full paths:
```python
config = initialize_config(
    llm_config_path="/full/path/to/OAI_CONFIG_LIST"
)
```

## Usage Questions

### How do I create my first agent?

```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

async def main():
    config = initialize_config()
    agent = SingleAssistant("Market_Analyst")
    response = await agent.chat("Get AAPL stock price")
    print(response.text)

asyncio.run(main())
```

### Why do I need async/await?

Agent Framework uses asynchronous operations for efficiency. All agent interactions must use `await`:

```python
# Correct
response = await agent.chat("message")

# Wrong - won't work
response = agent.chat("message")
```

### How do I run async code?

Wrap in `asyncio.run()`:

```python
import asyncio

async def my_function():
    # Your async code
    response = await agent.chat("message")

# Run it
asyncio.run(my_function())
```

### Which workflow should I use?

- **Simple queries**: SingleAssistant
- **Document analysis**: SingleAssistantRAG
- **Complex reports**: SingleAssistantShadow
- **Multiple perspectives**: MultiAssistant
- **Hierarchical tasks**: MultiAssistantWithLeader

See [Workflows Guide](../user-guide/workflows.md) for details.

### How do I reset conversation context?

```python
# Reset agent state
agent.reset()

# Now starts fresh conversation
response = await agent.chat("new topic")
```

### Can agents access real-time data?

Yes, if you have data source API keys configured:
- Stock prices (FinnHub, Yahoo Finance)
- Company financials (FMP)
- SEC filings (SEC API)
- News (FinnHub)

### How do I create custom agents?

```python
from finrobot.agents.agent_library import create_agent
from finrobot.config import get_config

config = {
    "name": "Custom_Analyst",
    "description": "My custom analyst",
    "instructions": "You are a specialized analyst...",
    "toolkits": ["market_data"]
}

client = get_config().get_chat_client()
agent = create_agent(config, chat_client=client)
```

## Error Messages

### "No module named 'agent_framework'"

Install Agent Framework:
```bash
pip install agent-framework --pre
```

### "API key not found"

1. Check `config_api_keys` file exists
2. Verify JSON format is valid
3. Ensure `OPENAI_API_KEY` is set

### "AsyncIO Event Loop Error"

Always use `asyncio.run()` for top-level async calls:
```python
# Correct
asyncio.run(main())

# Wrong - causes errors
await main()  # Only works inside async functions
```

### "Rate limit exceeded"

You've hit OpenAI rate limits. Solutions:
- Wait and retry
- Upgrade OpenAI plan
- Reduce request frequency

### "Invalid JSON in config file"

Validate JSON syntax:
```python
import json

with open("config_api_keys", "r") as f:
    json.load(f)  # Will show syntax errors
```

### "ChromaDB error" when using RAG

Install ChromaDB:
```bash
pip install chromadb
```

Or use specific version:
```bash
pip install chromadb==0.4.18
```

## Performance Questions

### How much does it cost to run?

Costs depend on OpenAI API usage:
- GPT-4: ~$0.03-0.06 per request (varies by length)
- GPT-3.5-turbo: ~$0.002-0.004 per request

Estimate: $1-5 for moderate daily usage

### How can I reduce costs?

1. Use GPT-3.5-turbo for simple queries
2. Reduce max_turns parameter
3. Reset context when appropriate
4. Cache common queries
5. Use SingleAssistant instead of MultiAssistant when possible

### Is it fast enough for production?

Yes, with considerations:
- Average response: 2-5 seconds
- Multi-agent workflows: 5-15 seconds
- Enable streaming for better UX
- Consider caching for common queries

### Can I run it locally?

Agent Framework supports local models via:
- Ollama integration
- Custom OpenAI-compatible APIs

Configure in `OAI_CONFIG_LIST` with local endpoint.

## Data Source Questions

### Do I need FinnHub API key?

No, it's optional. Without it:
- Basic stock data still available via Yahoo Finance
- Some features may have limited data

### What's the difference between FinnHub and FMP?

- **FinnHub**: Real-time data, news, company profiles
- **FMP**: Historical data, financial statements, ratios

Both useful; FinnHub for market data, FMP for fundamentals.

### Can I use my own data sources?

Yes! Create custom tools:

```python
from typing import Annotated
from pydantic import Field

def my_data_source(
    symbol: Annotated[str, Field(description="Stock symbol")]
) -> str:
    """Get data from my source."""
    # Your implementation
    return data

# Register tool in toolkit registry
```

### How often is data updated?

Depends on source:
- FinnHub: Real-time (15-minute delay for free tier)
- Yahoo Finance: 15-minute delay
- SEC: Updated as filings released

## Migration Questions

### How do I migrate from AutoGen?

See [Migration Guide](../migration/from-autogen.md) for complete instructions.

Key changes:
1. Update imports
2. Add async/await
3. Use workflow classes
4. Update response handling

### Are my AutoGen agents compatible?

Not directly, but migration is straightforward:
- Agent configurations similar
- Tool definitions need minor updates
- Workflows map to new patterns

### Will my AutoGen code break?

Yes, but migration is well-documented:
- [Migration Guide](../migration/from-autogen.md)
- [Migration Checklist](../migration/checklist.md)
- Code examples provided

## Advanced Questions

### Can I use multiple LLM providers?

Yes, configure different clients:

```python
from agent_framework.openai import OpenAIChatClient

client1 = OpenAIChatClient(model_id="gpt-4")
client2 = OpenAIChatClient(model_id="gpt-3.5-turbo")

agent1 = SingleAssistant("Agent1", chat_client=client1)
agent2 = SingleAssistant("Agent2", chat_client=client2)
```

### How do I implement streaming?

```python
async for chunk in agent.chat("message", stream=True):
    print(chunk.text, end="", flush=True)
```

### Can I save conversation history?

Yes, threads contain full history:

```python
# Access thread messages
messages = agent.thread.messages

# Save to file
import json
with open("conversation.json", "w") as f:
    json.dump([m.dict() for m in messages], f)
```

### How do I add observability?

Enable OpenTelemetry:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Detailed agent operations now logged
```

### Can I deploy to production?

Yes! Considerations:
- Use environment variables for secrets
- Implement error handling
- Add monitoring/logging
- Set rate limits
- Use caching
- Consider async workers

See [Production Guide](../advanced/production.md) for details.

## Troubleshooting

### Where can I get help?

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Review documentation
3. Search [GitHub Issues](https://github.com/AI4Finance-Foundation/FinRobot/issues)
4. Open new issue with details
5. Join [Discussions](https://github.com/AI4Finance-Foundation/FinRobot/discussions)

### How do I report bugs?

Open [GitHub Issue](https://github.com/AI4Finance-Foundation/FinRobot/issues) with:
- Python version
- FinRobot version
- Error message
- Code to reproduce
- Expected vs actual behavior

### Where's the complete documentation?

- [Documentation Home](../README.md)
- [Quick Start](../quick-start.md)
- [User Guide](../user-guide/agents.md)
- [Tutorials](../tutorials/01-market-analysis.md)
- [API Reference](../api/agents.md)

## Contributing

### Can I contribute?

Yes! Contributions welcome:
- Bug fixes
- New features
- Documentation
- Examples

See [Contributing Guide](contributing.md)

### How do I add new agents?

1. Add configuration to `agent_library.py`
2. Define tools if needed
3. Update documentation
4. Submit pull request

### How do I add new data sources?

1. Create utility module in `data_source/`
2. Define tool functions
3. Register in toolkit system
4. Add documentation
5. Submit PR

## Still Have Questions?

- Check [documentation](../README.md)
- Search [issues](https://github.com/AI4Finance-Foundation/FinRobot/issues)
- Ask in [discussions](https://github.com/AI4Finance-Foundation/FinRobot/discussions)
- Review [examples](../examples/basic.md)
