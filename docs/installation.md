# Installation Guide

Complete installation instructions for FinRobot-AF.

## System Requirements

### Software Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: 2GB free space

### API Requirements
- **Required**: OpenAI API key (or compatible LLM provider)
- **Optional**: Data source API keys (FinnHub, FMP, SEC)

## Installation Methods

### Method 1: uv Installation (Recommended) ⚡

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer (10-100x faster than pip).

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone repository
git clone https://github.com/IIIIQIIII/FinRobot-AF.git
cd FinRobot-AF

# 3. Create virtual environment and install (takes ~15 seconds)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install --pre -e .

# Optional: Install with development tools
uv pip install --pre -e ".[dev]"
```

**Why uv?**
- ⚡ **15 seconds** vs 5-10 minutes with conda/pip
- 🔒 Better dependency resolution
- 🎯 Modern pyproject.toml support
- 📦 Smaller disk footprint

### Method 2: Conda Installation

For users who prefer conda:

**Option A: Use installation script (Recommended)**

```bash
# Clone repository
git clone https://github.com/IIIIQIIII/FinRobot-AF.git
cd FinRobot-AF

# Run installation script
# Linux/macOS:
./scripts/install_conda.sh

# Windows:
scripts\install_conda.bat
```

**Option B: Manual installation**

```bash
# 1. Create conda environment
conda create -n finrobot python=3.10 -y
conda activate finrobot

# 2. Clone repository (if not already done)
git clone https://github.com/IIIIQIIII/FinRobot-AF.git
cd FinRobot-AF

# 3. Install dependencies with --pre flag (required for agent-framework)
pip install --pre -r requirements.txt

# 4. Install FinRobot in editable mode
pip install -e .
```

**Important**: The `--pre` flag is **required** because `agent-framework-core` is a pre-release package.

### Method 3: pip + venv Installation

Traditional Python virtual environment:

```bash
# 1. Clone repository
git clone https://github.com/IIIIQIIII/FinRobot-AF.git
cd FinRobot-AF

# 2. Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --pre -r requirements.txt
pip install -e .
```

### Method 4: PyPI Installation (Coming Soon)

When FinRobot-AF is published to PyPI:

```bash
# Install from PyPI
pip install finrobot-af

# Or with specific version
pip install finrobot-af==2.0.0
```

### Method 5: Docker Installation (Coming Soon)

```bash
# Pull Docker image
docker pull finrobot/finrobot-af:latest

# Run container
docker run -it -v $(pwd):/workspace finrobot/finrobot-af:latest
```

## Performance Comparison

| Method | Installation Time | Disk Usage | Notes |
|--------|------------------|------------|-------|
| **uv** | ~15 seconds | ~200MB | ⚡ Fastest, recommended |
| **pip** | 2-5 minutes | ~300MB | Standard |
| **conda** | 5-10 minutes | ~500MB+ | Good for system deps |

## Dependency Installation

### Core Dependencies

FinRobot-AF requires Microsoft Agent Framework and related packages:

```bash
# Install Agent Framework
pip install agent-framework --pre

# Core dependencies are installed automatically with requirements.txt:
# - agent-framework
# - openai
# - pandas
# - numpy
# - yfinance
# - chromadb (for RAG)
```

### Optional Dependencies

For enhanced functionality:

```bash
# For advanced charting
pip install plotly kaleido

# For PDF report generation
pip install reportlab pypdf

# For advanced NLP
pip install transformers torch

# For Jupyter notebook support
pip install jupyter ipykernel
```

## Configuration Setup

### 1. LLM Configuration (Required)

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

**Using Azure OpenAI:**
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

**Using Multiple Models:**
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

### 2. API Keys Configuration (Optional)

Create `config_api_keys` for data source access:

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

### 3. Environment Variables (Alternative)

Instead of config files, you can use environment variables:

```bash
# Linux/Mac
export OPENAI_API_KEY="sk-..."
export FINNHUB_API_KEY="your_key"

# Windows
set OPENAI_API_KEY=sk-...
set FINNHUB_API_KEY=your_key

# Or create .env file
echo 'OPENAI_API_KEY="sk-..."' > .env
echo 'FINNHUB_API_KEY="your_key"' >> .env
```

## Getting API Keys

### OpenAI API Key (Required)

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new secret key
5. Copy and save the key (shown only once)

**Cost**: Pay-as-you-go pricing, starts at $0.002/1K tokens

### FinnHub API Key (Optional)

1. Visit [FinnHub](https://finnhub.io/)
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 60 API calls/minute

**Features**: Stock prices, company profiles, news, financials

### Financial Modeling Prep (FMP) API Key (Optional)

1. Visit [FMP](https://financialmodelingprep.com/)
2. Create account
3. Get API key from dashboard
4. Free tier: 250 requests/day

**Features**: Advanced financial data, ratios, statements

### SEC API Key (Optional)

1. Visit [SEC API](https://sec-api.io/)
2. Sign up for account
3. Get API key
4. Free tier: 100 requests/day

**Features**: SEC filings, 10-K, 10-Q documents

## Verification

### Verify Installation

```python
# test_installation.py
import sys

def verify_installation():
    print(f"Python version: {sys.version}")

    try:
        import agent_framework
        print("✓ Agent Framework installed")
    except ImportError:
        print("✗ Agent Framework not found")
        return False

    try:
        import finrobot
        print("✓ FinRobot installed")
    except ImportError:
        print("✗ FinRobot not found")
        return False

    try:
        from finrobot.config import get_config
        config = get_config()
        print("✓ Config module working")
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

    print("\n✓ Installation verified successfully!")
    return True

if __name__ == "__main__":
    verify_installation()
```

Run verification:
```bash
python test_installation.py
```

### Test API Connection

```python
# test_api.py
import asyncio
from finrobot.config import initialize_config
from finrobot.agents.workflows import SingleAssistant

async def test_api():
    try:
        # Initialize config
        config = initialize_config()
        print("✓ Configuration loaded")

        # Create simple agent
        assistant = SingleAssistant("Data_Analyst")
        print("✓ Agent created")

        # Test simple query
        response = await assistant.chat("Hello, are you working?")
        print(f"✓ API connection successful")
        print(f"Response: {response.text[:100]}...")

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    asyncio.run(test_api())
```

Run test:
```bash
python test_api.py
```

## Platform-Specific Instructions

### macOS

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.10
brew install python@3.10

# Install Conda
brew install --cask miniconda

# Continue with standard installation
conda create -n finrobot python=3.10
conda activate finrobot
```

### Windows

```bash
# Install Miniconda from:
# https://docs.conda.io/en/latest/miniconda.html

# Open Anaconda Prompt and run:
conda create -n finrobot python=3.10
conda activate finrobot

# Continue with standard installation
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.10
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Continue with standard installation
conda create -n finrobot python=3.10
conda activate finrobot
```

## Troubleshooting Installation

### Issue: Agent Framework Installation Fails

```bash
# Try installing with explicit version
pip install agent-framework==0.0.1 --pre

# Or install from specific index
pip install --index-url https://pypi.org/simple agent-framework --pre
```

### Issue: ChromaDB Installation Error

```bash
# Install with specific version
pip install chromadb==0.4.18

# Or skip ChromaDB if not using RAG
pip install -r requirements.txt --no-deps
pip install agent-framework openai pandas yfinance
```

### Issue: Permission Denied

```bash
# Linux/Mac - use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue: SSL Certificate Error

```bash
# Temporary workaround (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Next Steps

After successful installation:

1. **[Quick Start Guide](quick-start.md)** - Create your first agent
2. **[Configuration Guide](configuration.md)** - Advanced configuration options
3. **[Tutorials](tutorials/01-market-analysis.md)** - Step-by-step examples

## Getting Help

If you encounter issues:

- Check [Troubleshooting Guide](reference/troubleshooting.md)
- Review [FAQ](reference/faq.md)
- Open an [issue on GitHub](https://github.com/IIIIQIIII/FinRobot-AF/issues)
- Join our [discussions](https://github.com/IIIIQIIII/FinRobot-AF/discussions)
