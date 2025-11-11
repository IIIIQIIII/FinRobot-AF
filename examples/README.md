# FinRobot-AF Examples

Workflow examples for sentiment analysis and FLS extraction on SEC 10-K filings.

## Available Examples

### 1. Sentiment Analysis Workflow

**File**: `sentiment_workflow.py`

Analyzes sentiment of policy discussions in 10-K Item 7 (MD&A) sections using a two-step agent pipeline.

**Features**:
- Config-driven workflow (`config/workflows/sentiment_analysis.json`)
- Step 1: Policy extraction using Policy_Extractor agent
- Step 2: Sentiment analysis using Sentiment_Analyzer agent
- Multi-LLM support (different providers per step)
- Structured JSON output with sentiment scores

**Usage**:
```bash
python examples/sentiment_workflow.py
```

**Example Output**:
```
Overall sentiment: optimistic
Sentiment score: +0.65
Policy segments: 8
```

**Output Location**: `results/sentiment/sentiment_{cik}_{year}.json`

---

### 2. FLS Extraction Workflow

**File**: `fls_workflow.py`

Extracts Forward-Looking Statements from 10-K filings using specialized agents for Section 7 (MD&A) and Section 1A (Risk Factors).

**Features**:
- Config-driven workflow (`config/workflows/fls_extraction.json`)
- Preliminary analysis with signal word detection (fast pre-screening)
- Deep analysis using FLS_MDA_Analyst and FLS_Risk_Analyst agents
- FLS categorization with reasoning
- Confidence scoring per segment

**Usage**:
```bash
python examples/fls_workflow.py
```

**Example Output**:
```
Section 7 (MD&A): 19 FLS
Section 1A (Risk): 31 FLS
Total FLS: 50

Preliminary candidates detected: 140
Final FLS after agent analysis: 50
```

**Output Location**: `results/fls_extraction/fls_{cik}_{year}.json`

---

### 3. Simple FLS Extraction (Rule-Based)

**File**: `simple_fls_extraction.py`

Fast, zero-cost FLS extraction using rule-based signal word pattern matching.

**Features**:
- No LLM required (zero API cost)
- 60+ FLS signal word patterns across 6 categories
- Batch processing support (process multiple filings)
- Historical statement filtering
- ~2 seconds per filing

**Usage**:
```bash
python examples/simple_fls_extraction.py
```

**Example Output**:
```
Section 7: 61 FLS (avg confidence: 0.878)
Section 1A: 79 FLS (avg confidence: 0.858)
Total: 140 FLS
Processing time: ~2 seconds
```

**Output Location**: `results/fls_extraction/fls_{cik}_{year}.json`

---

## Comparison Matrix

| Feature | Sentiment Workflow | FLS Workflow | Simple FLS |
|---------|-------------------|--------------|------------|
| **LLM Required** | Yes (2 agents) | Yes (2 agents) | No |
| **Speed** | ~30-45s | ~60-90s | ~2s |
| **Cost** | ~$0.01-0.03 | ~$0.02-0.05 | $0.00 |
| **Accuracy** | High | Very High | Good |
| **Output** | Sentiment + scores | FLS + categories + reasoning | FLS + confidence |
| **Use Case** | Sentiment analysis | Deep FLS analysis | Batch screening |
| **API Keys Needed** | Yes | Yes | No |

---

## Configuration

Workflow examples use JSON configuration files in `config/workflows/`:

### Sentiment Analysis Config
**File**: `config/workflows/sentiment_analysis.json`

```json
{
  "workflow_name": "sentiment_analysis",
  "paths": {
    "input_folder": "data/10k_filings",
    "output_folder": "results/sentiment"
  },
  "steps": {
    "extraction": {
      "provider": "openrouter",
      "model": "gpt-5",
      "temperature": 0.3,
      "agent_name": "Policy_Extractor"
    },
    "sentiment": {
      "provider": "aliyun",
      "model": "qwen3-max",
      "temperature": 0.5,
      "agent_name": "Sentiment_Analyzer"
    }
  }
}
```

### FLS Extraction Config
**File**: `config/workflows/fls_extraction.json`

```json
{
  "workflow_name": "fls_extraction",
  "paths": {
    "input_folder": "data/10k_filings",
    "output_folder": "results/fls_extraction"
  },
  "steps": {
    "mda_fls_extraction": {
      "provider": "aliyun",
      "model": "qwen3-max",
      "temperature": 0.3,
      "agent_name": "FLS_MDA_Analyst"
    },
    "risk_fls_extraction": {
      "provider": "aliyun",
      "model": "qwen3-max",
      "temperature": 0.3,
      "agent_name": "FLS_Risk_Analyst"
    }
  }
}
```

---

## Quick Start

### Prerequisites

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up API keys** (for workflow examples):
```bash
export OPENROUTER_API_KEY="your-key-here"
export DASHSCOPE_API_KEY="your-key-here"
```

3. **Prepare data**: Place 10-K filing JSON files in `data/10k_filings/`

Expected format: `{cik}_{year}.json`

Example: `1800_2020.json`

### Running Examples

**1. Sentiment Analysis**:
```bash
python examples/sentiment_workflow.py
```

**2. FLS Extraction (Agent-based)**:
```bash
python examples/fls_workflow.py
```

**3. FLS Extraction (Rule-based, no API needed)**:
```bash
python examples/simple_fls_extraction.py
```

---

## Output Structure

### Sentiment Analysis Output

```json
{
  "metadata": {
    "cik": "1800",
    "year": "2020",
    "company_name": "Abbott Laboratories",
    "analysis_timestamp": "2025-01-15T10:30:00"
  },
  "extraction": {
    "segments": [...]
  },
  "sentiment": {
    "overall_sentiment": "optimistic",
    "sentiment_score": 0.65,
    "reasoning": "..."
  },
  "summary": {
    "total_segments": 8,
    "overall_sentiment": "optimistic",
    "sentiment_score": 0.65
  }
}
```

### FLS Extraction Output

```json
{
  "metadata": {
    "cik": "1800",
    "year": "2020",
    "extraction_timestamp": "2025-01-15T10:30:00"
  },
  "section_7_mda": {
    "fls_count": 19,
    "fls_segments": [
      {
        "text": "We expect revenue growth of 5-7%...",
        "category": "revenue_guidance",
        "signal_words": ["expect"],
        "confidence": 0.95,
        "reasoning": "Clear future projection..."
      }
    ]
  },
  "section_1a_risks": {
    "fls_count": 31,
    "fls_segments": [...]
  },
  "combined_statistics": {
    "total_fls_extracted": 50,
    "mda_fls": 19,
    "risk_fls": 31
  }
}
```

---

## Best Practices

### When to Use Each Approach

**Use Sentiment Workflow when**:
- Analyzing management tone and outlook
- Tracking sentiment changes over time
- Research requiring sentiment context
- Investment decision support

**Use FLS Workflow when**:
- Deep analysis of forward-looking statements required
- Need categorization and reasoning for each FLS
- Quality and accuracy are more important than speed
- Research or compliance work

**Use Simple FLS when**:
- Screening 100+ filings quickly
- Cost is a constraint (no API budget)
- Need baseline/benchmark data
- Quick initial analysis before deep dive

### Recommended Workflow

1. **Screen** with Simple FLS (fast, free)
2. **Identify** high-interest filings (e.g., >50 FLS detected)
3. **Deep dive** with FLS Workflow (agent-based analysis)
4. **Analyze sentiment** with Sentiment Workflow (if needed)

---

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: Filing not found`
- **Solution**: Ensure filing exists in `data/10k_filings/{cik}_{year}.json`

**Issue**: `API key not found`
- **Solution**: Set environment variables for API keys

**Issue**: `No Section 7 (MD&A) found in filing`
- **Solution**: Check filing JSON has 'section_7' or 'item7_mda' key

**Issue**: `Agent timeout or slow response`
- **Solution**: Check network connection, try different LLM provider

---

## Additional Resources

- **Agent Library**: See `finrobot/agents/agent_library.py` for agent definitions
- **FLS Detection**: See `finrobot/functional/fls_detection.py` for signal word patterns
- **Workflow Pipeline**: See `finrobot/workflows/` for pipeline implementations
- **Configuration**: See `config/workflows/` for workflow config examples

---

## Example Data

The repository includes 5 sample 10-K filings in `data/10k_filings/`:

| CIK | Company | Year | Industry |
|-----|---------|------|----------|
| 1800 | Abbott Laboratories | 2020 | Healthcare |
| 1961 | Worlds Inc | 2020 | Technology |
| 2098 | Acme United Corp | 2020 | Consumer |
| 2178 | Innodata Inc | 2020 | Technology |
| 2186 | BK Technologies Corp | 2020 | Communications |

Run examples on any of these filings by changing the CIK and year in `main()` function.

---

**Last Updated**: 2025-01-15
