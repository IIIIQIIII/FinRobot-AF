"""
Data loader utilities for FinRobot-AF.
Handles loading and processing of 10-K filing data.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class TenKDataLoader:
    """Loader for 10-K filing JSON data."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize data loader.

        Args:
            data_dir: Path to data directory. Defaults to finrobot-af/data/10k_filings
        """
        if data_dir is None:
            # Default to finrobot-af/data/10k_filings
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            data_dir = project_root / "data" / "10k_filings"

        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise ValueError(f"Data directory not found: {self.data_dir}")

    def list_files(self) -> List[str]:
        """
        List all 10-K JSON files in data directory.

        Returns:
            List of filenames (e.g., ["2186_2020.json", ...])
        """
        json_files = sorted([
            f.name for f in self.data_dir.glob("*.json")
            if "_" in f.name  # Filter for CIK_YEAR.json pattern
        ])
        return json_files

    def load_filing(self, filename: str) -> Dict:
        """
        Load a single 10-K filing.

        Args:
            filename: Name of JSON file (e.g., "2186_2020.json")

        Returns:
            Dictionary containing filing data

        Example:
            >>> loader = TenKDataLoader()
            >>> data = loader.load_filing("2186_2020.json")
            >>> print(data['cik'], data['year'])
        """
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Filing not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def load_filing_by_cik_year(self, cik: str, year: str) -> Dict:
        """
        Load a filing by CIK and year.

        Args:
            cik: Company CIK (e.g., "2186")
            year: Filing year (e.g., "2020")

        Returns:
            Dictionary containing filing data
        """
        filename = f"{cik}_{year}.json"
        return self.load_filing(filename)

    def extract_item7(self, filing: Dict) -> Tuple[str, Dict]:
        """
        Extract Item 7 (MD&A) from a filing.

        Args:
            filing: Filing data dictionary

        Returns:
            Tuple of (item7_text, metadata)

        Example:
            >>> loader = TenKDataLoader()
            >>> filing = loader.load_filing("2186_2020.json")
            >>> item7_text, metadata = loader.extract_item7(filing)
            >>> print(f"Item 7 length: {len(item7_text)} chars")
        """
        item7_text = filing.get('section_7', '')

        metadata = {
            'cik': filing.get('cik', ''),
            'year': filing.get('year', ''),
            'filename': filing.get('filename', ''),
            'word_count': len(item7_text.split()),
            'char_count': len(item7_text)
        }

        return item7_text, metadata

    def load_all_item7s(self) -> List[Tuple[str, Dict]]:
        """
        Load Item 7 text from all available filings.

        Returns:
            List of (item7_text, metadata) tuples

        Example:
            >>> loader = TenKDataLoader()
            >>> all_item7s = loader.load_all_item7s()
            >>> print(f"Loaded {len(all_item7s)} filings")
        """
        results = []
        for filename in self.list_files():
            try:
                filing = self.load_filing(filename)
                item7_text, metadata = self.extract_item7(filing)
                results.append((item7_text, metadata))
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        return results

    def get_filing_info(self) -> List[Dict]:
        """
        Get summary information about all filings.

        Returns:
            List of dictionaries with filing metadata

        Example:
            >>> loader = TenKDataLoader()
            >>> info = loader.get_filing_info()
            >>> for filing in info:
            ...     print(f"{filing['cik']} ({filing['year']}): {filing['item7_words']} words")
        """
        info_list = []
        for filename in self.list_files():
            try:
                filing = self.load_filing(filename)
                item7_text, metadata = self.extract_item7(filing)

                info_list.append({
                    'filename': filename,
                    'cik': metadata['cik'],
                    'year': metadata['year'],
                    'item7_words': metadata['word_count'],
                    'item7_chars': metadata['char_count']
                })
            except Exception as e:
                print(f"Error reading {filename}: {e}")

        return info_list


class ResultWriter:
    """Writer for analysis results."""

    def __init__(self, results_dir: Optional[str] = None):
        """
        Initialize result writer.

        Args:
            results_dir: Path to results directory. Defaults to finrobot-af/results
        """
        if results_dir is None:
            # Default to finrobot-af/results
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            results_dir = project_root / "results"

        self.results_dir = Path(results_dir)
        self.extractions_dir = self.results_dir / "extractions"
        self.sentiments_dir = self.results_dir / "sentiments"

        # Create directories if they don't exist
        self.extractions_dir.mkdir(parents=True, exist_ok=True)
        self.sentiments_dir.mkdir(parents=True, exist_ok=True)

    def save_extraction(self, cik: str, year: str, extraction_data: Dict) -> str:
        """
        Save extraction results for a filing.

        Args:
            cik: Company CIK
            year: Filing year
            extraction_data: Extraction results dictionary

        Returns:
            Path to saved file
        """
        # Add metadata
        result = {
            'metadata': {
                'cik': cik,
                'year': year,
                'extraction_date': datetime.now().isoformat(),
                'agent': 'Policy_Extractor',
                'model': extraction_data.get('model', 'gpt-5')
            },
            **extraction_data
        }

        filename = self.extractions_dir / f"{cik}_{year}_extraction.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return str(filename)

    def save_sentiment(self, cik: str, year: str, sentiment_data: Dict) -> str:
        """
        Save sentiment analysis results for a filing.

        Args:
            cik: Company CIK
            year: Filing year
            sentiment_data: Sentiment analysis results dictionary

        Returns:
            Path to saved file
        """
        # Add metadata
        result = {
            'metadata': {
                'cik': cik,
                'year': year,
                'analysis_date': datetime.now().isoformat(),
                'agent': 'Sentiment_Analyzer',
                'model': sentiment_data.get('model', 'gpt-5')
            },
            **sentiment_data
        }

        filename = self.sentiments_dir / f"{cik}_{year}_sentiment.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return str(filename)

    def save_batch_summary(self, results: List[Dict], result_type: str) -> str:
        """
        Save batch processing summary to CSV.

        Args:
            results: List of result dictionaries
            result_type: 'extraction' or 'sentiment'

        Returns:
            Path to saved CSV file
        """
        import csv

        if result_type == 'extraction':
            filename = self.extractions_dir / "batch_extraction_summary.csv"
            fieldnames = ['cik', 'year', 'total_segments', 'policy_types', 'extraction_date', 'success']
        elif result_type == 'sentiment':
            filename = self.sentiments_dir / "batch_sentiment_summary.csv"
            fieldnames = ['cik', 'year', 'sentiment', 'score', 'confidence', 'analysis_date', 'success']
        else:
            raise ValueError(f"Unknown result_type: {result_type}")

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        return str(filename)


# Convenience functions
def load_10k_item7(cik: str, year: str) -> Tuple[str, Dict]:
    """
    Convenience function to load Item 7 by CIK and year.

    Args:
        cik: Company CIK
        year: Filing year

    Returns:
        Tuple of (item7_text, metadata)

    Example:
        >>> item7, meta = load_10k_item7("2186", "2020")
        >>> print(f"Loaded {meta['word_count']} words from {meta['cik']}")
    """
    loader = TenKDataLoader()
    filing = loader.load_filing_by_cik_year(cik, year)
    return loader.extract_item7(filing)


def list_available_filings() -> List[Dict]:
    """
    Convenience function to list all available filings.

    Returns:
        List of filing info dictionaries

    Example:
        >>> filings = list_available_filings()
        >>> for f in filings:
        ...     print(f"{f['cik']} ({f['year']}): {f['item7_words']} words")
    """
    loader = TenKDataLoader()
    return loader.get_filing_info()
