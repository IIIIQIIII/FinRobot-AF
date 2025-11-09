# Configuration Guide

Complete guide to configuring FinRobot-AF for your environment.

## Configuration Overview

FinRobot-AF uses two main configuration files:

1. **OAI_CONFIG_LIST** - LLM provider configuration
2. **config_api_keys** - Data source API keys

## LLM Configuration (OAI_CONFIG_LIST)

### Basic OpenAI Configuration

Create `OAI_CONFIG_LIST` in your project root:

```json
[
    {
        "model": "gpt-4",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1"
    }
]
```

### Azure OpenAI Configuration

```json
[
    {
        "model": "gpt-4",
        "api_key": "your-azure-key",
        "base_url": "https://your-resource.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2024-02-15-preview",
        "deployment_name": "gpt-4-deployment"
    }
]
```

### Multiple Model Configuration

```json
[
    {
        "model": "gpt-4",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1"
    },
    {
        "model": "gpt-3.5-turbo",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1"
    }
]
```

### Advanced Options

```json
[
    {
        "model": "gpt-4",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1",
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
]
```

## API Keys Configuration (config_api_keys)

### Full Configuration

Create `config_api_keys` in your project root:

```json
{
    "OPENAI_API_KEY": "sk-...",
    "FINNHUB_API_KEY": "your_finnhub_key",
    "FMP_API_KEY": "your_fmp_key",
    "SEC_API_KEY": "your_sec_key",
    "REDDIT_CLIENT_ID": "your_reddit_client_id",
    "REDDIT_CLIENT_SECRET": "your_reddit_client_secret"
}
```

### Minimal Configuration

For basic usage, only OpenAI key is required:

```json
{
    "OPENAI_API_KEY": "sk-..."
}
```

### Environment-Specific Configuration

Development:
```json
{
    "OPENAI_API_KEY": "sk-dev-...",
    "FINNHUB_API_KEY": "free_tier_key"
}
```

Production:
```json
{
    "OPENAI_API_KEY": "sk-prod-...",
    "FINNHUB_API_KEY": "premium_tier_key",
    "FMP_API_KEY": "enterprise_key"
}
```

## Environment Variables

### Using .env File

Create `.env` file:

```bash
# LLM Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Data Source APIs
FINNHUB_API_KEY=your_key
FMP_API_KEY=your_key
SEC_API_KEY=your_key

# Reddit API (optional)
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()

from finrobot.config import initialize_config
config = initialize_config()
```

### System Environment Variables

Linux/Mac:
```bash
export OPENAI_API_KEY="sk-..."
export FINNHUB_API_KEY="your_key"
```

Windows:
```bash
set OPENAI_API_KEY=sk-...
set FINNHUB_API_KEY=your_key
```

## Programmatic Configuration

### Using Config Object

```python
from finrobot.config import FinRobotConfig

# Create config
config = FinRobotConfig(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)

# Load configuration
config.load_api_keys()
config.load_llm_config()

# Get chat client
client = config.get_chat_client()

# Access API keys
finnhub_key = config.finnhub_api_key
fmp_key = config.fmp_api_key
```

### Global Configuration

```python
from finrobot.config import initialize_config, get_config

# Initialize once
initialize_config(
    api_keys_path="config_api_keys",
    llm_config_path="OAI_CONFIG_LIST"
)

# Access anywhere in code
config = get_config()
client = config.get_chat_client()
```

### Custom Chat Client

```python
from agent_framework.openai import OpenAIChatClient
from finrobot.agents.workflows import SingleAssistant

# Custom client with specific settings
client = OpenAIChatClient(
    model_id="gpt-4-turbo",
    api_key="sk-...",
    temperature=0.8,
    max_tokens=4000
)

# Use custom client
assistant = SingleAssistant(
    "Market_Analyst",
    chat_client=client
)
```

## Configuration for Different Environments

### Development Configuration

```python
# dev_config.py
from finrobot.config import initialize_config

def setup_dev_config():
    return initialize_config(
        api_keys_path="config_api_keys.dev",
        llm_config_path="OAI_CONFIG_LIST.dev"
    )
```

### Production Configuration

```python
# prod_config.py
from finrobot.config import initialize_config
import os

def setup_prod_config():
    # Use environment variables in production
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set")

    return initialize_config(
        api_keys_path=None,  # Use env vars
        llm_config_path="OAI_CONFIG_LIST.prod"
    )
```

### Conditional Configuration

```python
import os
from finrobot.config import initialize_config

# Determine environment
ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    config = initialize_config(
        llm_config_path="OAI_CONFIG_LIST.prod"
    )
elif ENV == "staging":
    config = initialize_config(
        llm_config_path="OAI_CONFIG_LIST.staging"
    )
else:
    config = initialize_config(
        llm_config_path="OAI_CONFIG_LIST.dev"
    )
```

## API Provider Configuration

### OpenAI

```json
{
    "model": "gpt-4",
    "api_key": "sk-...",
    "base_url": "https://api.openai.com/v1"
}
```

**Models Available**:
- `gpt-4` - Most capable
- `gpt-4-turbo` - Faster, lower cost
- `gpt-3.5-turbo` - Fast, economical

### Azure OpenAI

```json
{
    "model": "gpt-4",
    "api_key": "your-azure-key",
    "base_url": "https://your-resource.openai.azure.com/",
    "api_type": "azure",
    "api_version": "2024-02-15-preview",
    "deployment_name": "gpt-4"
}
```

### Custom OpenAI-Compatible API

```json
{
    "model": "custom-model",
    "api_key": "your-key",
    "base_url": "https://your-custom-endpoint.com/v1"
}
```

## Data Source Configuration

### FinnHub

```python
# In config_api_keys
{
    "FINNHUB_API_KEY": "your_key"
}
```

**Free Tier**: 60 calls/minute
**Paid Tiers**: Higher rate limits

**Features**:
- Stock prices
- Company profiles
- Financial news
- Earnings data

### Financial Modeling Prep (FMP)

```python
{
    "FMP_API_KEY": "your_key"
}
```

**Free Tier**: 250 requests/day
**Paid Tiers**: Higher limits, more endpoints

**Features**:
- Financial statements
- Stock ratios
- Historical data
- Company fundamentals

### SEC API

```python
{
    "SEC_API_KEY": "your_key"
}
```

**Free Tier**: 100 requests/day

**Features**:
- 10-K filings
- 10-Q filings
- 8-K filings
- Insider trading data

## Security Best Practices

### 1. Never Commit API Keys

Add to `.gitignore`:
```
config_api_keys
OAI_CONFIG_LIST
.env
*.secret
```

### 2. Use Environment Variables in Production

```python
import os

# Good: Use environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Bad: Hardcode keys
api_key = "sk-..."  # Never do this!
```

### 3. Rotate Keys Regularly

```python
# Update keys periodically
# Use different keys for dev/staging/prod
# Monitor usage in provider dashboards
```

### 4. Restrict Key Permissions

- Use read-only keys when possible
- Set spending limits
- Monitor usage alerts

### 5. Encrypt Config Files

```python
# Encrypt sensitive config files
# Use secrets management services (AWS Secrets Manager, Azure Key Vault)
```

## Configuration Validation

### Validate Configuration

```python
from finrobot.config import get_config

def validate_config():
    config = get_config()

    # Check API keys loaded
    assert config.openai_api_key, "OpenAI API key missing"

    # Check optional keys
    if config.finnhub_api_key:
        print("✓ FinnHub configured")
    else:
        print("⚠ FinnHub not configured (optional)")

    if config.fmp_api_key:
        print("✓ FMP configured")
    else:
        print("⚠ FMP not configured (optional)")

    # Test chat client
    try:
        client = config.get_chat_client()
        print("✓ Chat client created successfully")
    except Exception as e:
        print(f"✗ Chat client error: {e}")
        return False

    return True

validate_config()
```

### Test API Connections

```python
import asyncio
from finrobot.agents.workflows import SingleAssistant

async def test_connections():
    try:
        # Test LLM connection
        agent = SingleAssistant("Market_Analyst")
        response = await agent.chat("Hello")
        print(f"✓ LLM connection working")

        # Test data sources
        response = await agent.chat("Get AAPL stock price")
        print(f"✓ Data source connections working")

    except Exception as e:
        print(f"✗ Connection test failed: {e}")

asyncio.run(test_connections())
```

## Troubleshooting Configuration

### Issue: Config File Not Found

```python
# Error: FileNotFoundError: LLM config file not found

# Solution: Verify file exists in correct location
import os
print(os.getcwd())  # Check current directory
print(os.path.exists("OAI_CONFIG_LIST"))  # Verify file exists

# Or provide full path
config = initialize_config(
    llm_config_path="/full/path/to/OAI_CONFIG_LIST"
)
```

### Issue: API Key Not Loaded

```python
# Error: API key not found

# Solution 1: Check file format
# Ensure valid JSON syntax
# Ensure correct key names

# Solution 2: Load explicitly
from finrobot.config import get_config
config = get_config()
config.load_api_keys("config_api_keys")

# Solution 3: Set environment variable
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

### Issue: Invalid JSON

```python
# Error: JSONDecodeError

# Solution: Validate JSON
import json

with open("config_api_keys", "r") as f:
    try:
        data = json.load(f)
        print("✓ Valid JSON")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
```

## Advanced Configuration

### Custom Configuration Class

```python
from finrobot.config import FinRobotConfig

class CustomConfig(FinRobotConfig):
    def __init__(self):
        super().__init__()
        self.custom_setting = "value"

    def get_custom_client(self):
        # Custom client logic
        pass
```

### Configuration Profiles

```python
CONFIGS = {
    "development": {
        "llm_config": "OAI_CONFIG_LIST.dev",
        "api_keys": "config_api_keys.dev"
    },
    "production": {
        "llm_config": "OAI_CONFIG_LIST.prod",
        "api_keys": "config_api_keys.prod"
    }
}

def load_profile(profile: str):
    settings = CONFIGS[profile]
    return initialize_config(
        llm_config_path=settings["llm_config"],
        api_keys_path=settings["api_keys"]
    )
```

## Next Steps

- **[Quick Start](quick-start.md)** - Get started with configured system
- **[Installation](installation.md)** - Installation instructions
- **[Security](advanced/security.md)** - Security best practices
- **[FAQ](reference/faq.md)** - Common configuration questions
