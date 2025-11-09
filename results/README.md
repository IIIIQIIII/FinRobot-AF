# FinRobot-AF Results Directory

Analysis results and outputs from FinAgent processing pipeline.

## Directory Structure

```
results/
├── extractions/           # Policy extraction results
│   ├── {CIK}_{YEAR}_extraction.json
│   └── batch_extraction_summary.csv
│
├── sentiments/            # Sentiment analysis results
│   ├── {CIK}_{YEAR}_sentiment.json
│   └── batch_sentiment_summary.csv
│
└── README.md              # This file
```

## File Formats

### Extraction Results (`{CIK}_{YEAR}_extraction.json`)
```json
{
  "metadata": {
    "cik": "string",
    "year": "string",
    "extraction_date": "ISO 8601 datetime",
    "agent": "Policy_Extractor",
    "model": "gpt-5"
  },
  "extracted_segments": [
    {
      "segment_id": 1,
      "text": "Full text of extracted segment",
      "policy_type": "monetary|fiscal|trade|tax|regulatory",
      "keywords": ["keyword1", "keyword2"],
      "confidence": 0.95
    }
  ],
  "summary": "Brief summary of all policy mentions",
  "statistics": {
    "total_segments": 5,
    "avg_segment_length": 250,
    "policy_types_found": ["monetary", "fiscal"]
  }
}
```

### Sentiment Results (`{CIK}_{YEAR}_sentiment.json`)
```json
{
  "metadata": {
    "cik": "string",
    "year": "string",
    "analysis_date": "ISO 8601 datetime",
    "agent": "Sentiment_Analyzer",
    "model": "gpt-5"
  },
  "overall_sentiment": "optimistic|pessimistic|neutral",
  "sentiment_score": -0.65,
  "confidence": 0.88,
  "reasoning": "Management expresses concerns about...",
  "segment_sentiments": [
    {
      "segment_id": 1,
      "sentiment": "pessimistic",
      "score": -0.7,
      "reasoning": "..."
    }
  ]
}
```

### Batch Summary CSV

**Extraction Summary** (`batch_extraction_summary.csv`):
```csv
cik,year,total_segments,policy_types,extraction_date,success
2186,2020,5,"monetary;fiscal",2025-11-08T10:30:00Z,true
```

**Sentiment Summary** (`batch_sentiment_summary.csv`):
```csv
cik,year,sentiment,score,confidence,analysis_date,success
2186,2020,pessimistic,-0.65,0.88,2025-11-08T10:35:00Z,true
```

## Naming Convention

- Individual results: `{CIK}_{YEAR}_{type}.json`
- Batch summaries: `batch_{type}_summary.csv`
- Type: `extraction` or `sentiment`

## Result Retention

- Individual JSON files: Permanent (detailed analysis)
- CSV summaries: Updated with each batch run
- Backup old summaries before overwriting

## Export Formats

### For Analysis
- **CSV**: Batch summaries for statistical analysis
- **JSON**: Individual files for detailed review
- **Excel**: Combined results (generated on demand)

### For Reporting
- **Markdown**: Human-readable reports
- **PDF**: Final presentation (generated on demand)

---

*Updated: 2025-11-08*
*FinAgent System - FinRobot-AF*
