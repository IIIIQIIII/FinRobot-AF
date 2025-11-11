# Forward-Looking Statement (FLS) Extraction from 10-K Filings

## Overview

This guide demonstrates how to extract and classify Forward-Looking Statements (FLS) from SEC 10-K filings using FinRobot-AF's specialized FLS agents and toolkits.

### What is a Forward-Looking Statement?

A forward-looking statement is any statement that projects, anticipates, or discusses future events, plans, expectations, or outcomes rather than describing historical facts. These statements are prospective in nature and involve uncertainty.

### Key FLS Signal Words

- **Planning**: anticipates, intends, plans, seeks, aims
- **Expectations**: expects, believes, continues, guidance, outlook
- **Possibility**: could, may, might, possibly, potential
- **Projections**: estimates, projects, prospects, forecasts
- **Likelihood**: should, will, would, likely
- **Future periods**: next quarter, fiscal 2024, going forward, in the future

## Architecture

### Components

1. **FLS Agents**
   - `FLS_MDA_Analyst`: Extracts FLS from Section 7 (Management's Discussion & Analysis)
   - `FLS_Risk_Analyst`: Extracts FLS from Section 1A (Risk Factors)

2. **FLS Detection Toolkit** (`finrobot/toolkits/fls_detection.py`)
   - Signal word detection
   - FLS scoring and confidence calculation
   - Sentence extraction with context
   - Category classification

3. **Workflow Configuration** (`config/workflows/fls_extraction.json`)
   - Configurable LLM providers per step
   - Customizable parameters (temperature, max_tokens)
   - Input/output path management

## Quick Start

### 1. Test FLS Detection (No LLM Required)

First, verify the FLS detection toolkit works with rule-based detection:

```bash
cd /Users/jason/Projects/FinRobot-AF
.venv/bin/python tests/test_fls_detection.py
```

**Output:**
```
============================================================
FLS DETECTION TOOLKIT TEST SUITE
============================================================

TEST 1: Signal Word Detection
[1] We expect revenue to grow 5-7% in the next fiscal year.
    Signals: {'expectations': ['expect']}
    FLS Score: 1.000
    Likely FLS: ✓

TEST 5: Real 10-K Filing Analysis
Filing: Abbott Laboratories (CIK: 1800, Year: 2020)
Section 7 length: 72,253 characters
Section 1A length: 28,627 characters

--- Section 7 (MD&A) Analysis ---
FLS found: 16
Avg confidence: 0.866

--- Section 1A (Risk Factors) Analysis ---
FLS found: 64
Avg confidence: 0.808
```

### 2. Run Full FLS Extraction with LLM Agents

```bash
cd /Users/jason/Projects/FinRobot-AF
.venv/bin/python examples/fls_extraction_10k.py
```

## Configuration

### Workflow Configuration: `config/workflows/fls_extraction.json`

```json
{
  "workflow_name": "fls_extraction",
  "description": "Forward-Looking Statement extraction from 10-K filings",

  "steps": {
    "mda_fls_extraction": {
      "description": "Extract FLS from Section 7 (MD&A)",
      "llm_provider": "aliyun",
      "llm_model": "qwen3-max",
      "temperature": 0.3,
      "max_tokens": 6000,
      "agent_name": "FLS_MDA_Analyst",
      "section": "section_7"
    },
    "risk_fls_extraction": {
      "description": "Extract FLS from Section 1A (Risk Factors)",
      "llm_provider": "aliyun",
      "llm_model": "qwen3-max",
      "temperature": 0.3,
      "max_tokens": 6000,
      "agent_name": "FLS_Risk_Analyst",
      "section": "section_1A"
    }
  },

  "paths": {
    "input_folder": "data/10k_filings",
    "output_folder": "results/fls_extraction",
    "save_intermediate": true
  },

  "options": {
    "save_mda_extraction": true,
    "save_risk_extraction": true,
    "create_combined_output": true,
    "min_fls_confidence": 0.5,
    "max_segments_per_section": 50,
    "verbose": true
  }
}
```

## FLS Categories

### Section 7 (MD&A) Categories

| Category | Description | Example |
|----------|-------------|---------|
| `revenue_guidance` | Revenue/earnings projections | "We expect revenue to grow 5-7% in fiscal 2024" |
| `strategic` | Strategic initiatives and plans | "The company plans to expand into Asian markets" |
| `market_outlook` | Market expectations | "We believe demand will remain strong" |
| `operational` | Operational improvements | "We plan to improve manufacturing efficiency" |
| `capital` | Capital allocation plans | "We intend to increase dividends by 10%" |
| `risk_mitigation` | Risk mitigation strategies | "We will implement hedging strategies" |

### Section 1A (Risk Factors) Categories

| Category | Description | Example |
|----------|-------------|---------|
| `market` | Market and competitive risks | "Increased competition could reduce our market share" |
| `operational` | Operational risks | "Supply chain disruptions could affect operations" |
| `financial` | Financial risks | "Rising interest rates would increase debt costs" |
| `regulatory` | Regulatory and legal risks | "Regulatory changes may require compliance costs" |
| `strategic` | Strategic execution risks | "Technology failures could impact strategy" |
| `external` | External/geopolitical risks | "Economic downturn may reduce demand" |

## Programmatic Usage

### Example 1: Basic FLS Detection

```python
from finrobot.toolkits.fls_detection import (
    detect_fls_signal_words,
    calculate_fls_score,
    analyze_fls_in_text
)

text = """
We expect revenue to grow 5-7% in the next fiscal year.
The company plans to expand operations in Asia-Pacific markets.
Management believes the new product will capture 20% market share.
"""

# Detect signal words
signals = detect_fls_signal_words(text)
print(f"Signals: {signals}")
# Output: {'expectations': ['expect', 'believes'], 'planning': ['plans'], 'likelihood': ['will']}

# Calculate FLS score
score = calculate_fls_score(text)
print(f"FLS Score: {score}")
# Output: 1.000

# Full analysis
analysis = analyze_fls_in_text(text, "Sample MD&A")
print(f"Total FLS found: {analysis['total_fls_found']}")
```

### Example 2: Workflow-based Extraction

```python
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.fls_extraction_10k import FLSExtractionWorkflow

async def main():
    # Initialize workflow with configuration
    workflow = FLSExtractionWorkflow("fls_extraction")

    # Extract FLS from Abbott Laboratories 2020 10-K
    output_file = await workflow.analyze_filing("1800", "2020")

    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 3: Custom Agent Usage

```python
import asyncio
from finrobot.config import FinRobotConfig
from finrobot.agents.agent_library import create_agent
from finrobot.llm_config import switch_provider

async def extract_fls_custom():
    # Configure LLM
    switch_provider("aliyun", "qwen3-max")

    config = FinRobotConfig()
    chat_client = config.get_chat_client()

    # Create FLS agent
    agent = create_agent("FLS_MDA_Analyst", chat_client)

    # Prepare prompt
    prompt = """
    Analyze this MD&A text and extract FLS:

    "Looking ahead to fiscal 2024, we expect revenue growth of 8-10%
    driven by new product launches. The company plans to invest $500M
    in R&D and expand manufacturing capacity."

    Extract all forward-looking statements with signal words and categories.
    """

    # Run analysis
    response = await agent.chat(prompt)
    print(response.text)

asyncio.run(extract_fls_custom())
```

## Output Format

### Combined Output: `results/fls_extraction/fls_1800_2020.json`

```json
{
  "metadata": {
    "cik": "1800",
    "year": "2020",
    "filename": "1800_2020",
    "extraction_timestamp": "2025-01-15T10:30:00",
    "workflow": "fls_extraction"
  },
  "section_7_mda": {
    "fls_count": 16,
    "summary": "MD&A contains FLS about revenue growth, strategic initiatives...",
    "fls_segments": [
      {
        "segment_id": 1,
        "text": "We expect continued growth in diagnostics...",
        "fls_category": "revenue_guidance",
        "signal_words": ["expect"],
        "confidence": 0.92,
        "reasoning": "Clear future projection with explicit timeline"
      }
    ]
  },
  "section_1a_risks": {
    "fls_count": 64,
    "summary": "Risk Factors contain FLS about market risks, regulatory changes...",
    "fls_segments": [
      {
        "segment_id": 1,
        "text": "Increased competition could reduce our market share...",
        "fls_category": "market",
        "signal_words": ["could"],
        "risk_type": "Competitive pressure",
        "confidence": 0.88,
        "reasoning": "Hypothetical future event with projected impact"
      }
    ]
  },
  "combined_statistics": {
    "total_fls_extracted": 80,
    "mda_fls": 16,
    "risk_fls": 64
  }
}
```

## Testing

### Run Test Suite

```bash
# Test FLS detection toolkit
.venv/bin/python tests/test_fls_detection.py

# Expected output:
# ✓ Signal word detection
# ✓ Sentence extraction
# ✓ Full analysis on sample text
# ✓ FLS categorization
# ✓ Real 10-K filing analysis (Abbott 2020)
```

## Customization

### Adding Custom Signal Words

Edit `finrobot/toolkits/fls_detection.py`:

```python
FLS_SIGNAL_WORDS = {
    "planning": [
        "anticipate", "intend", "plan", "seek", "aim",
        "target",  # Add custom word
    ],
    # ... other categories
}
```

### Creating Custom FLS Categories

```python
def classify_fls_category_custom(text: str) -> str:
    """Custom FLS categorization."""
    text_lower = text.lower()

    # ESG initiatives
    if any(word in text_lower for word in ['sustainability', 'esg', 'carbon']):
        return 'esg_initiatives'

    # M&A activity
    if any(word in text_lower for word in ['acquisition', 'merger', 'acquire']):
        return 'ma_activity'

    return 'other'
```

### Adjusting Confidence Thresholds

In `config/workflows/fls_extraction.json`:

```json
{
  "options": {
    "min_fls_confidence": 0.7,  // Increase for higher precision
    "max_segments_per_section": 100  // Increase for more results
  }
}
```

## Best Practices

### 1. Temperature Settings

- **Extraction tasks**: Use low temperature (0.2-0.3) for consistent, precise extraction
- **Analysis tasks**: Use moderate temperature (0.5) for balanced reasoning

### 2. Token Limits

- **Section 7 (MD&A)**: 6000-8000 tokens (typically 60-80k characters)
- **Section 1A (Risk Factors)**: 4000-6000 tokens (typically 20-40k characters)

### 3. LLM Provider Selection

| Provider | Best For | Cost | Speed |
|----------|----------|------|-------|
| Aliyun (Qwen3-Max) | High-volume extraction | Low | Fast |
| OpenRouter (GPT-5) | High-precision analysis | High | Medium |
| OpenAI (GPT-4) | Critical accuracy tasks | High | Medium |

### 4. Validation Workflow

1. **Test with toolkit first**: Use `tests/test_fls_detection.py` to verify signal word detection
2. **Sample analysis**: Run on 1-2 filings with verbose mode
3. **Validate output**: Check extracted FLS manually
4. **Batch processing**: Run on full dataset once validated

## Troubleshooting

### Issue: No FLS Found

**Cause**: Text may be historical or confidence threshold too high

**Solution**:
```json
// Lower confidence threshold in config
"options": {
  "min_fls_confidence": 0.3
}
```

### Issue: Too Many False Positives

**Cause**: Signal words appearing in historical context

**Solution**: The toolkit filters historical statements automatically, but you can adjust:
```python
# In fls_detection.py
def is_historical_statement(text: str) -> bool:
    # Add more historical indicators
    historical_indicators = [
        r'\b(was|were|had|did|increased|decreased)\b',
        r'\b(recorded|recognized|reported)\b',
        # Add custom patterns
    ]
```

### Issue: JSON Parsing Error from Agent

**Cause**: Agent response contains non-JSON text

**Solution**: The workflow automatically falls back to toolkit-based extraction. To improve:
- Use lower temperature (0.2-0.3)
- Add explicit JSON format instructions in agent prompt
- Use more capable LLM (GPT-4/5 vs smaller models)

## Performance Benchmarks

### Abbott Laboratories 2020 10-K

- **Section 7 (MD&A)**: 72,253 chars → 16 FLS segments (0.866 avg confidence)
- **Section 1A (Risk Factors)**: 28,627 chars → 64 FLS segments (0.808 avg confidence)
- **Processing time**: ~30 seconds with Qwen3-Max
- **Cost**: ~$0.02 per filing (Aliyun pricing)

## References

- **Agent Library**: `finrobot/agents/agent_library.py` (Lines 307-481)
- **FLS Toolkit**: `finrobot/toolkits/fls_detection.py`
- **Workflow Config**: `config/workflows/fls_extraction.json`
- **Example Script**: `examples/fls_extraction_10k.py`
- **Test Suite**: `tests/test_fls_detection.py`

## Related Documentation

- [Agent Library Reference](../api/agents.md)
- [Workflow Configuration Guide](../configuration.md)
- [10-K Filing Structure](./10k_filing_structure.md)

---

**Last Updated**: 2025-01-15
**Version**: 1.0.0
**Status**: Production Ready
