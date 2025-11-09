# Agents API Reference

Complete API reference for FinRobot agents module.

## Module: finrobot.agents.agent_library

### create_agent()

Create an agent from configuration.

```python
def create_agent(
    agent_config: str | Dict[str, Any],
    chat_client: Optional[ChatClient] = None,
    toolkit_registry: Optional[Dict] = None
) -> ChatAgent
```

**Parameters**:
- `agent_config` (str | dict): Agent name or configuration dictionary
- `chat_client` (ChatClient, optional): Custom chat client instance
- `toolkit_registry` (dict, optional): Custom toolkit registry

**Returns**:
- `ChatAgent`: Configured agent instance

**Example**:
```python
from finrobot.agents.agent_library import create_agent
from finrobot.config import get_config

# By name
agent = create_agent("Market_Analyst")

# With custom client
client = get_config().get_chat_client()
agent = create_agent("Market_Analyst", chat_client=client)

# With custom config
config = {
    "name": "Custom_Agent",
    "description": "My custom agent",
    "instructions": "You are a helpful assistant",
    "toolkits": ["market_data"]
}
agent = create_agent(config, chat_client=client)
```

### create_default_toolkit_registry()

Create default toolkit registry with all available tools.

```python
def create_default_toolkit_registry() -> Dict[str, List[Callable]]
```

**Returns**:
- `dict`: Dictionary mapping toolkit names to tool lists

**Example**:
```python
from finrobot.agents.agent_library import create_default_toolkit_registry

registry = create_default_toolkit_registry()
print(registry.keys())  # ['market_data', 'financial_analysis', ...]
```

### AGENT_CONFIGS

Dictionary containing pre-configured agent definitions.

**Available Agents**:
- `Market_Analyst`: Market data and forecasting specialist
- `Expert_Investor`: Investment analysis and reporting
- `Financial_Analyst`: Financial metrics and statements
- `Data_Analyst`: Python data analysis
- `Statistician`: Statistical modeling
- `Software_Developer`: Python programming
- `Programmer`: General programming
- `IT_Specialist`: Technical problem-solving
- `Accountant`: Accounting principles
- `Artificial_Intelligence_Engineer`: AI/ML tasks

**Example**:
```python
from finrobot.agents.agent_library import AGENT_CONFIGS

# View agent configuration
config = AGENT_CONFIGS["Market_Analyst"]
print(config["name"])
print(config["description"])
print(config["instructions"])
print(config["toolkits"])
```

## Module: finrobot.agents.workflows

### SingleAssistant

Basic single-agent workflow pattern.

```python
class SingleAssistant(WorkflowBase):
    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client: Optional[ChatClient] = None,
        toolkit_registry: Optional[Dict] = None,
        max_turns: int = 10,
        **kwargs
    )
```

**Parameters**:
- `agent_config`: Agent name or configuration dict
- `chat_client`: Optional custom chat client
- `toolkit_registry`: Optional custom toolkit registry
- `max_turns`: Maximum conversation turns (default: 10)

**Methods**:

#### chat()
```python
async def chat(
    self,
    message: str,
    stream: bool = False,
    **kwargs
) -> Response
```

Execute workflow with given message.

**Parameters**:
- `message` (str): User message
- `stream` (bool): Enable streaming responses (default: False)

**Returns**:
- `Response`: Agent response object

**Example**:
```python
from finrobot.agents.workflows import SingleAssistant

assistant = SingleAssistant("Market_Analyst")
response = await assistant.chat("Get AAPL price")
print(response.text)

# Streaming
async for chunk in assistant.chat("Analyze TSLA", stream=True):
    print(chunk.text, end="")
```

#### reset()
```python
def reset(self) -> None
```

Reset workflow state by creating new thread.

**Example**:
```python
assistant.reset()
```

### SingleAssistantRAG

Agent with retrieval-augmented generation.

```python
class SingleAssistantRAG(WorkflowBase):
    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        docs_path: str,
        collection_name: str = "default",
        chat_client: Optional[ChatClient] = None,
        toolkit_registry: Optional[Dict] = None,
        embedding_model: str = "text-embedding-ada-002",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        k: int = 5,
        **kwargs
    )
```

**Parameters**:
- `agent_config`: Agent name or config
- `docs_path`: Path to documents directory
- `collection_name`: ChromaDB collection name
- `chat_client`: Optional custom client
- `toolkit_registry`: Optional toolkit registry
- `embedding_model`: Embedding model name
- `chunk_size`: Document chunk size
- `chunk_overlap`: Overlap between chunks
- `k`: Number of documents to retrieve

**Example**:
```python
from finrobot.agents.workflows import SingleAssistantRAG

rag_agent = SingleAssistantRAG(
    agent_config="Expert_Investor",
    docs_path="./financial_reports",
    collection_name="q4_earnings",
    k=5
)

response = await rag_agent.chat(
    "What are the key revenue trends in Q4 reports?"
)
```

### SingleAssistantShadow

Dual-agent planning and execution pattern.

```python
class SingleAssistantShadow(WorkflowBase):
    def __init__(
        self,
        agent_config: str | Dict[str, Any],
        chat_client: Optional[ChatClient] = None,
        toolkit_registry: Optional[Dict] = None,
        **kwargs
    )
```

**Parameters**:
- `agent_config`: Agent configuration
- `chat_client`: Optional custom client
- `toolkit_registry`: Optional toolkit registry

**Example**:
```python
from finrobot.agents.workflows import SingleAssistantShadow

shadow_agent = SingleAssistantShadow("Expert_Investor")

response = await shadow_agent.chat(
    "Create comprehensive investment analysis for MSFT"
)
```

### MultiAssistant

Group chat with multiple agents.

```python
class MultiAssistant(WorkflowBase):
    def __init__(
        self,
        agents_config: List[str | Dict[str, Any]],
        chat_client: Optional[ChatClient] = None,
        toolkit_registry: Optional[Dict] = None,
        max_rounds: int = 5,
        **kwargs
    )
```

**Parameters**:
- `agents_config`: List of agent names or configs
- `chat_client`: Optional custom client
- `toolkit_registry`: Optional toolkit registry
- `max_rounds`: Maximum discussion rounds

**Example**:
```python
from finrobot.agents.workflows import MultiAssistant

team = MultiAssistant([
    "Market_Analyst",
    "Financial_Analyst",
    "Statistician"
])

response = await team.chat(
    "Comprehensive analysis of NVDA from all perspectives"
)
```

### MultiAssistantWithLeader

Hierarchical multi-agent coordination.

```python
class MultiAssistantWithLeader(WorkflowBase):
    def __init__(
        self,
        leader_config: str | Dict[str, Any],
        team_configs: List[str | Dict[str, Any]],
        chat_client: Optional[ChatClient] = None,
        toolkit_registry: Optional[Dict] = None,
        max_rounds: int = 3,
        **kwargs
    )
```

**Parameters**:
- `leader_config`: Leader agent configuration
- `team_configs`: List of team member configs
- `chat_client`: Optional custom client
- `toolkit_registry`: Optional toolkit registry
- `max_rounds`: Maximum coordination rounds

**Example**:
```python
from finrobot.agents.workflows import MultiAssistantWithLeader

workflow = MultiAssistantWithLeader(
    leader_config="Financial_Analyst",
    team_configs=["Data_Analyst", "Statistician", "Market_Analyst"]
)

response = await workflow.chat(
    "Complete financial analysis of Tesla with team"
)
```

## Response Objects

### Response

Response object returned by agent interactions.

**Attributes**:
- `text` (str): Response text content
- `messages` (list): All conversation messages
- `usage` (dict): Token usage information
- `metadata` (dict): Additional metadata

**Example**:
```python
response = await agent.chat("message")

print(response.text)        # Main response text
print(response.usage)       # Token counts
print(response.messages)    # Full message history
```

## Module: finrobot.config

### FinRobotConfig

Configuration management class.

```python
class FinRobotConfig:
    def __init__(
        self,
        api_keys_path: Optional[str] = None,
        llm_config_path: Optional[str] = None
    )
```

**Methods**:

#### load_api_keys()
```python
def load_api_keys(self, path: Optional[str] = None) -> None
```

Load API keys from JSON file.

#### load_llm_config()
```python
def load_llm_config(self, path: Optional[str] = None) -> Dict[str, Any]
```

Load LLM configuration from JSON file.

#### get_chat_client()
```python
def get_chat_client(self, model_id: Optional[str] = None) -> ChatClient
```

Get or create OpenAI chat client.

#### get_api_key()
```python
def get_api_key(self, key_name: str) -> Optional[str]
```

Get API key by name.

**Properties**:
- `finnhub_api_key`: FinnHub API key
- `fmp_api_key`: FMP API key
- `sec_api_key`: SEC API key
- `openai_api_key`: OpenAI API key

**Example**:
```python
from finrobot.config import FinRobotConfig

config = FinRobotConfig(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)

config.load_api_keys()
config.load_llm_config()

client = config.get_chat_client()
finnhub_key = config.finnhub_api_key
```

### initialize_config()

Initialize global configuration.

```python
def initialize_config(
    api_keys_path: Optional[str] = None,
    llm_config_path: Optional[str] = None,
    auto_load: bool = True
) -> FinRobotConfig
```

**Parameters**:
- `api_keys_path`: Path to API keys file
- `llm_config_path`: Path to LLM config file
- `auto_load`: Auto-load configuration

**Returns**:
- `FinRobotConfig`: Initialized configuration

**Example**:
```python
from finrobot.config import initialize_config

config = initialize_config(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)
```

### get_config()

Get global configuration instance.

```python
def get_config() -> FinRobotConfig
```

**Returns**:
- `FinRobotConfig`: Global configuration instance

**Example**:
```python
from finrobot.config import get_config

config = get_config()
client = config.get_chat_client()
```

## Module: finrobot.toolkits

### get_tools_from_config()

Get tools for agent from toolkit configuration.

```python
def get_tools_from_config(
    toolkit_names: List[str],
    toolkit_registry: Dict[str, List[Callable]]
) -> List[Callable]
```

**Parameters**:
- `toolkit_names`: List of toolkit names
- `toolkit_registry`: Toolkit registry dictionary

**Returns**:
- `list`: List of tool functions

**Example**:
```python
from finrobot.toolkits import get_tools_from_config
from finrobot.agents.agent_library import create_default_toolkit_registry

registry = create_default_toolkit_registry()
tools = get_tools_from_config(["market_data"], registry)
```

### create_tool_from_function()

Create tool from Python function.

```python
def create_tool_from_function(func: Callable) -> Callable
```

**Parameters**:
- `func`: Python function

**Returns**:
- `Callable`: Tool function

**Example**:
```python
from typing import Annotated
from pydantic import Field
from finrobot.toolkits import create_tool_from_function

def my_tool(
    symbol: Annotated[str, Field(description="Stock symbol")]
) -> str:
    """My custom tool."""
    return f"Result for {symbol}"

tool = create_tool_from_function(my_tool)
```

## Type Definitions

### Agent Configuration Dictionary

```python
{
    "name": str,                    # Agent name
    "description": str,             # Agent description
    "instructions": str,            # System instructions
    "toolkits": List[str]          # List of toolkit names
}
```

### LLM Configuration Dictionary

```python
{
    "model": str,                   # Model ID
    "api_key": str,                 # API key
    "base_url": str,                # API base URL
    "temperature": float,           # Temperature (optional)
    "max_tokens": int,              # Max tokens (optional)
    "top_p": float,                 # Top-p (optional)
    "api_type": str,                # API type (optional, for Azure)
    "api_version": str              # API version (optional, for Azure)
}
```

### Toolkit Registry Dictionary

```python
{
    "toolkit_name": [               # Toolkit name as key
        function1,                  # Tool functions as values
        function2,
        ...
    ]
}
```

## Constants

### Default Values

```python
DEFAULT_MAX_TURNS = 10              # Default max conversation turns
DEFAULT_MAX_ROUNDS = 5              # Default max multi-agent rounds
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_K_DOCUMENTS = 5
```

## See Also

- [Workflows API](workflows.md) - Workflow classes reference
- [Config API](config.md) - Configuration API reference
- [Toolkits API](toolkits.md) - Tools and toolkits reference
- [User Guide](../user-guide/agents.md) - Agent usage guide
