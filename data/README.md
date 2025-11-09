# FinRobot-AF Data Directory

Standardized data organization for FinAgent system and financial analysis.

## Directory Structure

```
data/
├── 10k_filings/           # 10-K annual report data (JSON files)
│   └── {CIK}_{YEAR}.json
│
└── README.md              # This file
```

## File Naming Convention

### 10-K Filings
- **Format**: `{CIK}_{YEAR}.json`
- **Example**: `2186_2020.json`
- **CIK**: SEC Central Index Key (company identifier)
- **YEAR**: Fiscal year of the filing

## Data Schema

### Raw 10-K JSON Structure
```json
{
  "filename": "string",
  "cik": "string",
  "year": "string",
  "section_1": "string",
  "section_1A": "string",
  "section_1B": "string",
  "section_2": "string",
  "section_3": "string",
  "section_4": "string",
  "section_5": "string",
  "section_6": "string",
  "section_7": "string",      // Item 7: MD&A (target for analysis)
  "section_7A": "string",
  "section_8": "string",
  "section_9": "string",
  "section_9A": "string",
  "section_9B": "string",
  "section_10": "string",
  "section_11": "string",
  "section_12": "string",
  "section_13": "string",
  "section_14": "string",
  "section_15": "string"
}
```

**Note**: Processed results (extraction and sentiment) are stored in the `results/` directory, not here.

## Usage Guidelines

### Adding New 10-K Files
1. Place JSON files in `10k_filings/`
2. Follow naming convention: `{CIK}_{YEAR}.json`
3. Ensure JSON contains `section_7` field (Item 7: MD&A)
4. Run FinAgent pipeline to analyze

### Data Quality
- **Encoding**: UTF-8
- **Format**: Valid JSON
- **Required Fields**: `cik`, `year`, `section_7`
- **Text Cleaning**: Remove HTML tags, normalize whitespace

## Sample Data

Current dataset:
- 5 10-K filings from 2020
- Companies: CIK 1800, 1961, 2098, 2178, 2186
- Average Item 7 length: ~6,000-10,000 words

## Data Privacy & Compliance

- All data sourced from public SEC EDGAR filings
- No proprietary or confidential information
- Compliant with SEC data usage policies
- For research and analysis purposes only

---

*Updated: 2025-11-08*
*FinAgent System - FinRobot-AF*
