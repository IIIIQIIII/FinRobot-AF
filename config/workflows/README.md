# Workflow Configurations

This directory contains configurable workflow definitions for FinRobot-AF.

## Overview

Workflows allow you to configure:
- **Different LLM providers per step** (e.g., GPT-5 for extraction, Qwen3-Max for sentiment)
- **LLM parameters** (temperature, max_tokens) per step
- **Input/output paths**
- **Save options**

## Available Workflows

### sentiment_analysis.json

Financial sentiment analysis with two steps:

1. **Extraction**: Extract policy segments from 10-K Item 7
2. **Sentiment**: Analyze sentiment of extracted policies

**Default Configuration**:
- Extraction: OpenRouter GPT-5 (temperature: 0.3)
- Sentiment: Aliyun Qwen3-Max (temperature: 0.5)

## Configuration Structure

```json
{
  "workflow_name": "sentiment_analysis",
  "description": "Description of what this workflow does",

  "steps": {
    "step_name": {
      "description": "What this step does",
      "llm_provider": "aliyun",
      "llm_model": "qwen3-max",
      "temperature": 0.5,
      "max_tokens": 2000,
      "agent_name": "Agent_Name"
    }
  },

  "paths": {
    "input_folder": "data/10k_filings",
    "output_folder": "results/sentiment",
    "save_intermediate": true
  },

  "options": {
    "save_extraction": true,
    "save_sentiment": true,
    "create_summary": true,
    "verbose": true
  }
}
```

## Step Configuration

### LLM Settings

| Parameter      | Type   | Description                          | Example         |
|----------------|--------|--------------------------------------|-----------------|
| llm_provider   | string | Provider ID (aliyun, openrouter, etc)| "aliyun"        |
| llm_model      | string | Model name from provider config      | "qwen3-max"     |
| temperature    | float  | Sampling temperature (0.0-2.0)       | 0.5             |
| max_tokens     | int    | Maximum tokens to generate           | 2000            |
| agent_name     | string | Agent name for logging               | "Extractor"     |

### Path Configuration

| Parameter        | Type   | Description                    |
|------------------|--------|--------------------------------|
| input_folder     | string | Where to find input files      |
| output_folder    | string | Where to save results          |
| save_intermediate| bool   | Save intermediate results      |

### Options

| Parameter        | Type | Description                       |
|------------------|------|-----------------------------------|
| save_extraction  | bool | Save extraction results           |
| save_sentiment   | bool | Save sentiment results            |
| create_summary   | bool | Print summary after completion    |
| verbose          | bool | Print detailed progress           |

## Usage

### Load and Run Workflow

```python
from finrobot.workflow_config import WorkflowConfig
from examples.configurable_sentiment_analysis import ConfigurableSentimentWorkflow

# Initialize with workflow config
workflow = ConfigurableSentimentWorkflow("sentiment_analysis")

# Run on a filing
output_file = await workflow.analyze_filing("1800", "2020")
```

### Get Workflow Configuration

```python
from finrobot.workflow_config import load_workflow

# Load config
config = load_workflow("sentiment_analysis")

# Get step configuration
extraction_config = config.get_llm_config("extraction")
print(f"Provider: {extraction_config['provider']}")
print(f"Model: {extraction_config['model']}")
print(f"Temperature: {extraction_config['temperature']}")

# Get paths
paths = config.get_paths()
print(f"Input: {paths['input_folder']}")
print(f"Output: {paths['output_folder']}")
```

## Creating Custom Workflows

### 1. Copy Sample File

```bash
cp sentiment_analysis.sample.json my_custom_workflow.json
```

### 2. Edit Configuration

```json
{
  "workflow_name": "my_custom_workflow",
  "steps": {
    "extraction": {
      "llm_provider": "openai",
      "llm_model": "gpt-4",
      "temperature": 0.2
    },
    "sentiment": {
      "llm_provider": "aliyun",
      "llm_model": "qwen-turbo",
      "temperature": 0.7
    }
  }
}
```

### 3. Use in Code

```python
workflow = ConfigurableSentimentWorkflow("my_custom_workflow")
await workflow.analyze_filing("1800", "2020")
```

## Example Configurations

### High Quality (Slow, Expensive)

```json
{
  "steps": {
    "extraction": {
      "llm_provider": "openrouter",
      "llm_model": "gpt-5",
      "temperature": 0.2,
      "max_tokens": 8000
    },
    "sentiment": {
      "llm_provider": "openrouter",
      "llm_model": "claude-3",
      "temperature": 0.3,
      "max_tokens": 4000
    }
  }
}
```

### Fast & Cost-Effective

```json
{
  "steps": {
    "extraction": {
      "llm_provider": "aliyun",
      "llm_model": "qwen-turbo",
      "temperature": 0.5,
      "max_tokens": 2000
    },
    "sentiment": {
      "llm_provider": "aliyun",
      "llm_model": "qwen-plus",
      "temperature": 0.5,
      "max_tokens": 1000
    }
  }
}
```

### Balanced (Default)

```json
{
  "steps": {
    "extraction": {
      "llm_provider": "openrouter",
      "llm_model": "gpt-5",
      "temperature": 0.3,
      "max_tokens": 4000
    },
    "sentiment": {
      "llm_provider": "aliyun",
      "llm_model": "qwen3-max",
      "temperature": 0.5,
      "max_tokens": 2000
    }
  }
}
```

## Temperature Guidelines

| Temperature | Use Case                                    |
|-------------|---------------------------------------------|
| 0.0 - 0.3   | Extraction, factual tasks                   |
| 0.4 - 0.6   | Balanced analysis (sentiment)               |
| 0.7 - 1.0   | Creative tasks, diverse outputs             |
| 1.0+        | Highly creative (not recommended for finance)|

## Provider Selection

| Provider    | Strengths                  | Cost      | Speed  |
|-------------|----------------------------|-----------|--------|
| Aliyun      | Chinese data, cost-effective| Low       | Fast   |
| OpenRouter  | Multiple models, flexible  | Medium    | Medium |
| OpenAI      | High quality, reliable     | High      | Medium |

## Tips

1. **Use conservative temperature for extraction** (0.2-0.3) to ensure factual accuracy
2. **Use moderate temperature for sentiment** (0.4-0.6) for balanced analysis
3. **Test different providers** to find optimal quality/cost balance
4. **Save intermediate results** for debugging
5. **Use verbose mode** during development

## Files

- `sentiment_analysis.json` - Active configuration
- `sentiment_analysis.sample.json` - Template file
- `README.md` - This file

## See Also

- [LLM Provider Configuration](../../config/llm_providers.json)
- [Environment Setup](../../ENV_SETUP.md)
- [Configurable Workflow Example](../../examples/configurable_sentiment_analysis.py)
