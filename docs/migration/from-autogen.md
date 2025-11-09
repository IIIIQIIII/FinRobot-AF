# Migration from AutoGen to Agent Framework

Complete guide for migrating FinRobot code from AutoGen to Microsoft Agent Framework.

## Overview

This guide helps you migrate existing FinRobot AutoGen code to the new Agent Framework architecture. The migration involves key conceptual and API changes.

## Key Differences

### Architecture Changes

| Aspect | AutoGen | Agent Framework |
|--------|---------|-----------------|
| **State Management** | Implicit (GroupChat state) | Explicit (AgentThread) |
| **Agent Execution** | Synchronous default | Async/await required |
| **Tool Execution** | Single-turn default | Multi-turn default |
| **Orchestration** | GroupChat classes | Builder patterns & workflows |
| **Response Handling** | Direct replies | Response objects |
| **Configuration** | llm_config dict | Chat client objects |

### Conceptual Mapping

**AutoGen Concepts → Agent Framework Concepts**

| AutoGen | Agent Framework |
|---------|-----------------|
| AssistantAgent | ChatAgent |
| UserProxyAgent | User input / AgentThread |
| GroupChat | MultiAssistant workflow |
| GroupChatManager | Workflow coordinator |
| initiate_chat() | workflow.chat() |
| generate_reply() | agent.run() |
| register_function() | Tool registration |
| llm_config | ChatClient |

## Migration Steps

### Step 1: Update Imports

**Before (AutoGen):**
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from finrobot.agents.workflow import SingleAssistant
```

**After (Agent Framework):**
```python
from agent_framework import ChatAgent, AgentThread
from finrobot.agents.workflows import SingleAssistant, MultiAssistant
from finrobot.config import initialize_config
```

### Step 2: Configuration Setup

**Before (AutoGen):**
```python
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": "sk-..."
        }
    ],
    "temperature": 0.7
}
```

**After (Agent Framework):**
```python
# Option 1: Use config files
config = initialize_config(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)
client = config.get_chat_client()

# Option 2: Direct client creation
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    model_id="gpt-4",
    api_key="sk-...",
    temperature=0.7
)
```

### Step 3: Agent Creation

**Before (AutoGen):**
```python
from finrobot.agents.workflow import SingleAssistant

assistant = SingleAssistant(
    name="Market_Analyst",
    llm_config=llm_config
)

# Chat with agent
response = assistant.chat("Analyze AAPL")
```

**After (Agent Framework):**
```python
from finrobot.agents.workflows import SingleAssistant

# Initialize config first
config = initialize_config()

# Create assistant (config loaded globally)
assistant = SingleAssistant("Market_Analyst")

# Chat with agent (now async)
response = await assistant.chat("Analyze AAPL")
print(response.text)
```

### Step 4: Async/Await Migration

All agent interactions are now asynchronous.

**Before (AutoGen):**
```python
def analyze_stock(symbol):
    assistant = SingleAssistant("Market_Analyst", llm_config)
    result = assistant.chat(f"Analyze {symbol}")
    return result

# Call directly
result = analyze_stock("AAPL")
```

**After (Agent Framework):**
```python
async def analyze_stock(symbol):
    assistant = SingleAssistant("Market_Analyst")
    result = await assistant.chat(f"Analyze {symbol}")
    return result.text

# Call with asyncio
import asyncio
result = asyncio.run(analyze_stock("AAPL"))
```

### Step 5: Multi-Agent Migration

**Before (AutoGen):**
```python
from autogen import GroupChat, GroupChatManager

analyst1 = AssistantAgent("Market_Analyst", llm_config=llm_config)
analyst2 = AssistantAgent("Financial_Analyst", llm_config=llm_config)
user_proxy = UserProxyAgent("User", ...)

groupchat = GroupChat(
    agents=[user_proxy, analyst1, analyst2],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="Analyze AAPL")
```

**After (Agent Framework):**
```python
from finrobot.agents.workflows import MultiAssistant

# Create multi-agent team
team = MultiAssistant([
    "Market_Analyst",
    "Financial_Analyst"
])

# Collaborative analysis
response = await team.chat("Analyze AAPL from multiple perspectives")
print(response.text)
```

### Step 6: Tool Registration

**Before (AutoGen):**
```python
def get_stock_price(symbol: str) -> str:
    """Get stock price."""
    return f"Price for {symbol}"

assistant.register_function(
    function_map={
        "get_stock_price": get_stock_price
    }
)
```

**After (Agent Framework):**
```python
from typing import Annotated
from pydantic import Field

def get_stock_price(
    symbol: Annotated[str, Field(description="Stock symbol")]
) -> str:
    """Get stock price."""
    return f"Price for {symbol}"

# Tools registered via toolkit system
# See toolkits.py for tool registration
```

### Step 7: Response Handling

**Before (AutoGen):**
```python
response = assistant.chat("Get AAPL price")
# response is dict with 'content', 'role', etc.
print(response['content'])
```

**After (Agent Framework):**
```python
response = await assistant.chat("Get AAPL price")
# response is Response object
print(response.text)

# Access additional info
print(response.messages)  # All messages
print(response.usage)     # Token usage
```

## Complete Migration Examples

### Example 1: Single Assistant Migration

**Before (AutoGen):**
```python
from finrobot.agents.workflow import SingleAssistant

llm_config = {
    "config_list": [{
        "model": "gpt-4",
        "api_key": "sk-..."
    }]
}

assistant = SingleAssistant("Market_Analyst", llm_config)
response = assistant.chat("Analyze NVDA stock")
print(response['content'])
```

**After (Agent Framework):**
```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

async def main():
    # Initialize config
    config = initialize_config(
        llm_config_path="OAI_CONFIG_LIST"
    )

    # Create assistant
    assistant = SingleAssistant("Market_Analyst")

    # Chat (now async)
    response = await assistant.chat("Analyze NVDA stock")
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: RAG Migration

**Before (AutoGen):**
```python
from finrobot.agents.workflow import SingleAssistantRAG

assistant = SingleAssistantRAG(
    name="Expert_Investor",
    llm_config=llm_config,
    docs_path="./reports"
)

response = assistant.chat("Analyze earnings reports")
```

**After (Agent Framework):**
```python
import asyncio
from finrobot.agents.workflows import SingleAssistantRAG

async def main():
    assistant = SingleAssistantRAG(
        agent_config="Expert_Investor",
        docs_path="./reports"
    )

    response = await assistant.chat("Analyze earnings reports")
    print(response.text)

asyncio.run(main())
```

### Example 3: Multi-Agent Migration

**Before (AutoGen):**
```python
from finrobot.agents.workflow import MultiAssistant

team = MultiAssistant(
    agents=["Market_Analyst", "Financial_Analyst"],
    llm_config=llm_config
)

result = team.chat("Comprehensive TSLA analysis")
```

**After (Agent Framework):**
```python
import asyncio
from finrobot.agents.workflows import MultiAssistant

async def main():
    team = MultiAssistant([
        "Market_Analyst",
        "Financial_Analyst"
    ])

    result = await team.chat("Comprehensive TSLA analysis")
    print(result.text)

asyncio.run(main())
```

## Common Migration Issues

### Issue 1: Synchronous to Async

**Problem**: Code runs synchronously
```python
# This won't work
response = assistant.chat("message")  # Missing await
```

**Solution**: Add async/await
```python
# Correct
async def my_function():
    response = await assistant.chat("message")
    return response.text

# Run with asyncio
import asyncio
result = asyncio.run(my_function())
```

### Issue 2: Response Format

**Problem**: Expecting dict response
```python
response = await assistant.chat("message")
text = response['content']  # AttributeError
```

**Solution**: Use response object attributes
```python
response = await assistant.chat("message")
text = response.text  # Correct
```

### Issue 3: Configuration

**Problem**: Passing llm_config directly
```python
# Old way - won't work
assistant = SingleAssistant("Agent", llm_config=llm_config)
```

**Solution**: Use global config or chat_client
```python
# Option 1: Global config
config = initialize_config()
assistant = SingleAssistant("Agent")

# Option 2: Custom client
from agent_framework.openai import OpenAIChatClient
client = OpenAIChatClient(model_id="gpt-4", api_key="...")
assistant = SingleAssistant("Agent", chat_client=client)
```

### Issue 4: Tool Registration

**Problem**: Old register_function pattern
```python
assistant.register_function(function_map={"tool": my_tool})
```

**Solution**: Tools registered via toolkit system
```python
# Tools are pre-registered in toolkits.py
# For custom tools, modify toolkit registry
from finrobot.toolkits import create_default_toolkit_registry

registry = create_default_toolkit_registry()
registry["custom_tools"] = [my_tool]

assistant = SingleAssistant("Agent", toolkit_registry=registry)
```

## Migration Checklist

Use this checklist to ensure complete migration:

- [ ] Updated all imports from `autogen` to `agent_framework`
- [ ] Changed imports from `finrobot.agents.workflow` to `finrobot.agents.workflows`
- [ ] Created configuration files (`OAI_CONFIG_LIST`, `config_api_keys`)
- [ ] Added `initialize_config()` call at startup
- [ ] Converted all agent interactions to async/await
- [ ] Updated response handling (dict → object)
- [ ] Wrapped main code in `asyncio.run()`
- [ ] Migrated GroupChat to MultiAssistant
- [ ] Updated tool registration if using custom tools
- [ ] Tested all workflows
- [ ] Updated error handling for async operations
- [ ] Verified API key configuration works

## Testing Your Migration

### Basic Test
```python
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

async def test_migration():
    # Test config
    config = initialize_config()
    assert config is not None, "Config initialization failed"

    # Test agent creation
    agent = SingleAssistant("Market_Analyst")
    assert agent is not None, "Agent creation failed"

    # Test chat
    response = await agent.chat("Hello")
    assert response.text, "Chat failed"

    print("✓ Migration test passed!")

asyncio.run(test_migration())
```

### Workflow Test
```python
async def test_workflows():
    # Test all workflow patterns
    from finrobot.agents.workflows import (
        SingleAssistant,
        SingleAssistantRAG,
        SingleAssistantShadow,
        MultiAssistant
    )

    # SingleAssistant
    sa = SingleAssistant("Market_Analyst")
    r1 = await sa.chat("Test")
    assert r1.text

    # MultiAssistant
    ma = MultiAssistant(["Market_Analyst", "Financial_Analyst"])
    r2 = await ma.chat("Test")
    assert r2.text

    print("✓ All workflows working!")

asyncio.run(test_workflows())
```

## Performance Considerations

### Token Usage
Agent Framework may use different token counts:
- Multi-turn tool execution (more tokens)
- Explicit thread management (more messages)
- Plan before execution in Shadow pattern

### Optimization Tips
```python
# Reduce max_turns for simple queries
assistant = SingleAssistant("Agent", max_turns=5)

# Reset thread between unrelated queries
assistant.reset()

# Use simpler workflows when possible
# SingleAssistant instead of MultiAssistant for single-perspective tasks
```

## Getting Help

If you encounter migration issues:

1. Check [FAQ](../reference/faq.md)
2. Review [Troubleshooting Guide](../reference/troubleshooting.md)
3. See [Examples](../examples/basic.md)
4. Open [GitHub Issue](https://github.com/AI4Finance-Foundation/FinRobot/issues)

## Next Steps

After migration:
- [ ] Review [Workflows Guide](../user-guide/workflows.md)
- [ ] Explore [Agent Guide](../user-guide/agents.md)
- [ ] Try [Tutorials](../tutorials/01-market-analysis.md)
- [ ] Read [Best Practices](../advanced/performance.md)
