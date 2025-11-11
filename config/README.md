# LLM Provider Configuration

This directory contains configuration for multiple LLM providers.

## Security Notice

**⚠️ API keys are now stored in `.env` file for security.**

See [ENV_SETUP.md](../ENV_SETUP.md) for complete setup instructions.

## Quick Start

### 1. Setup Environment Variables

```bash
# Copy sample file
cp .env.sample .env

# Edit .env with your actual API keys
nano .env
```

### 2. Use Providers

```python
from finrobot.llm_config import switch_provider

# Switch to Aliyun Qwen
switch_provider("aliyun", "qwen3-max")

# Switch to OpenRouter
switch_provider("openrouter", "gpt-5")

# Switch to OpenAI Direct
switch_provider("openai", "gpt-4")
```

## Configuration File

**File**: `llm_providers.json`

### Structure

```json
{
  "providers": {
    "provider_name": {
      "name": "Display Name",
      "base_url": "https://api.endpoint.com/v1",
      "api_key": "your-api-key",
      "models": {
        "model-alias": "actual-model-id",
        "default": "default-model-id"
      }
    }
  },
  "active_provider": "current_provider",
  "active_model": "current_model"
}
```

## Supported Providers

### 1. Aliyun DashScope

**Provider ID**: `aliyun`

**Models**:
- `qwen3-max` - Latest Qwen 3 model (most capable)
- `qwen-plus` - Fast and balanced
- `qwen-turbo` - Fastest, lower cost

**Base URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`

### 2. OpenRouter

**Provider ID**: `openrouter`

**Models**:
- `gpt-5` - OpenAI GPT-5 via OpenRouter
- `gpt-4` - OpenAI GPT-4 via OpenRouter
- `claude-3` - Anthropic Claude 3 Opus

**Base URL**: `https://openrouter.ai/api/v1`

### 3. OpenAI Direct

**Provider ID**: `openai`

**Models**:
- `gpt-4` - GPT-4
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5` - GPT-3.5 Turbo

**Base URL**: `https://api.openai.com/v1`

**Note**: Requires `OPENAI_API_KEY` environment variable

## Usage

### In Code

```python
from finrobot.config import FinRobotConfig
from finrobot.llm_config import switch_provider

# Switch provider
switch_provider("aliyun", "qwen3-max")

# Initialize FinRobot
config = FinRobotConfig()
client = config.get_chat_client()  # Uses active provider

# Or get config directly
from finrobot.llm_config import get_llm_config
llm_config = get_llm_config()
# Returns: {"model": "qwen-max", "api_key": "...", "base_url": "..."}
```

### List Available Providers

```python
from finrobot.llm_config import LLMConfigManager

mgr = LLMConfigManager()
mgr.list_providers()
```

### CLI

```bash
# Test configuration
python test_llm_config.py

# Run sentiment analysis with Qwen
python examples/test_sentiment_qwen.py
```

## Adding New Providers

Edit `llm_providers.json`:

```json
{
  "providers": {
    "your_provider": {
      "name": "Your Provider Name",
      "base_url": "https://your-api.com/v1",
      "api_key": "your-api-key-or-${ENV_VAR}",
      "models": {
        "model1": "actual-model-id-1",
        "model2": "actual-model-id-2",
        "default": "actual-model-id-1"
      }
    }
  }
}
```

Then use:

```python
switch_provider("your_provider", "model1")
```

## Environment Variables

API keys can reference environment variables:

```json
{
  "api_key": "${OPENAI_API_KEY}"
}
```

The system will automatically load from `os.getenv("OPENAI_API_KEY")`.

## Test Results

### Aliyun Qwen-Max (qwen3-max)

**Test**: Abbott Laboratories 2020 10-K Sentiment Analysis

```
Extraction:  5 segments
Sentiment:   optimistic (+0.75)
Confidence:  0.95
Performance: ~1.5 minutes
Status:      ✅ Working
```

## Files

- `llm_providers.json` - Provider configuration
- `README.md` - This file
- `../test_llm_config.py` - Configuration test script
- `../examples/test_sentiment_qwen.py` - Qwen sentiment test

## Notes

- Configuration changes are saved automatically
- Active provider/model persists across sessions
- All providers use OpenAI-compatible API format
- FinRobot-AF automatically uses the active provider
