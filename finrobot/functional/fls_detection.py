"""
FLS (Forward-Looking Statement) Detection Toolkit for FinRobot-AF.

This module provides tools for detecting and analyzing forward-looking statements
in financial documents (10-K filings).
"""

import re
from typing import List, Dict, Tuple, Optional
import json


# FLS Signal Words Database
FLS_SIGNAL_WORDS = {
    "planning": [
        "anticipate", "anticipates", "anticipated", "anticipating",
        "intend", "intends", "intended", "intending",
        "plan", "plans", "planned", "planning",
        "seek", "seeks", "seeking",
        "aim", "aims", "aiming"
    ],
    "expectations": [
        "expect", "expects", "expected", "expecting",
        "believe", "believes", "believed", "believing",
        "continue", "continues", "continuing",
        "guidance", "outlook", "forecast", "forecasts", "forecasting"
    ],
    "possibility": [
        "could", "may", "might", "possibly", "potential", "potentially"
    ],
    "projections": [
        "estimate", "estimates", "estimated", "estimating",
        "project", "projects", "projected", "projecting",
        "prospect", "prospects"
    ],
    "likelihood": [
        "should", "will", "would", "shall", "likely"
    ],
    "future_periods": [
        "next quarter", "next year", "fiscal 2024", "fiscal 2025",
        "going forward", "in the future", "future period", "upcoming",
        "near term", "long term", "over time"
    ]
}

# Flatten for quick lookup
ALL_SIGNAL_WORDS = set()
for category in FLS_SIGNAL_WORDS.values():
    ALL_SIGNAL_WORDS.update([w.lower() for w in category])


def detect_fls_signal_words(text: str) -> Dict[str, List[str]]:
    """
    Detect FLS signal words in text.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary mapping signal word categories to found words

    Example:
        >>> text = "We expect revenue to grow and plan to expand operations."
        >>> detect_fls_signal_words(text)
        {'expectations': ['expect'], 'planning': ['plan']}
    """
    text_lower = text.lower()
    found_signals = {}

    for category, words in FLS_SIGNAL_WORDS.items():
        found_in_category = []
        for word in words:
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_in_category.append(word)

        if found_in_category:
            found_signals[category] = found_in_category

    return found_signals


def calculate_fls_score(text: str) -> float:
    """
    Calculate FLS likelihood score (0.0 to 1.0) based on signal word density.

    Args:
        text: Input text to analyze

    Returns:
        Float score between 0.0 (no FLS indicators) and 1.0 (high FLS likelihood)
    """
    if not text or len(text.strip()) == 0:
        return 0.0

    signals = detect_fls_signal_words(text)
    total_signals = sum(len(words) for words in signals.values())

    # Normalize by text length (signals per 100 words)
    word_count = len(text.split())
    if word_count == 0:
        return 0.0

    signal_density = (total_signals / word_count) * 100

    # Cap at 1.0, scale appropriately (5+ signals per 100 words = high FLS)
    score = min(signal_density / 5.0, 1.0)

    return round(score, 3)


def extract_sentences_with_signals(
    text: str,
    min_signals: int = 1,
    context_sentences: int = 0
) -> List[Dict[str, any]]:
    """
    Extract sentences containing FLS signal words.

    Args:
        text: Input text to analyze
        min_signals: Minimum number of signal words required
        context_sentences: Number of surrounding sentences to include for context

    Returns:
        List of dictionaries with sentence text, signals found, and scores
    """
    # Simple sentence splitting (can be improved with NLTK)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    results = []

    for i, sentence in enumerate(sentences):
        signals = detect_fls_signal_words(sentence)
        total_signals = sum(len(words) for words in signals.values())

        if total_signals >= min_signals:
            # Get context sentences if requested
            start_idx = max(0, i - context_sentences)
            end_idx = min(len(sentences), i + context_sentences + 1)
            context_text = ' '.join(sentences[start_idx:end_idx])

            results.append({
                'sentence_id': i,
                'text': sentence.strip(),
                'context': context_text.strip() if context_sentences > 0 else None,
                'signal_words': signals,
                'signal_count': total_signals,
                'fls_score': calculate_fls_score(sentence)
            })

    return results


def is_historical_statement(text: str) -> bool:
    """
    Check if text appears to be a historical statement (not forward-looking).

    Args:
        text: Text to analyze

    Returns:
        True if text appears historical, False otherwise
    """
    historical_indicators = [
        # Past tense verbs
        r'\b(was|were|had|did|increased|decreased|grew|declined|reported)\b',
        # Historical time references
        r'\b(last year|prior year|previous quarter|in 20\d{2}|as of|ended)\b',
        # Financial statement references
        r'\b(recorded|recognized|incurred|realized)\b',
    ]

    text_lower = text.lower()

    for pattern in historical_indicators:
        if re.search(pattern, text_lower):
            return True

    return False


def filter_non_fls(candidates: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Filter out likely non-FLS statements from candidates.

    Args:
        candidates: List of candidate FLS segments

    Returns:
        Filtered list with non-FLS statements removed
    """
    filtered = []

    for candidate in candidates:
        text = candidate.get('text', '')

        # Skip if clearly historical
        if is_historical_statement(text):
            continue

        # Skip if no strong FLS signals
        if candidate.get('fls_score', 0) < 0.1:
            continue

        filtered.append(candidate)

    return filtered


def analyze_fls_in_text(
    text: str,
    section_name: str = "Unknown",
    min_confidence: float = 0.3
) -> Dict[str, any]:
    """
    Comprehensive FLS analysis of text.

    Args:
        text: Text to analyze
        section_name: Name of the section (e.g., "Section 7 - MD&A")
        min_confidence: Minimum FLS score to include in results

    Returns:
        Dictionary with analysis results
    """
    # Extract sentences with FLS signals
    candidates = extract_sentences_with_signals(text, min_signals=1, context_sentences=1)

    # Filter non-FLS
    fls_segments = filter_non_fls(candidates)

    # Further filter by confidence
    fls_segments = [s for s in fls_segments if s['fls_score'] >= min_confidence]

    # Calculate statistics
    total_segments = len(fls_segments)
    avg_score = sum(s['fls_score'] for s in fls_segments) / total_segments if total_segments > 0 else 0.0

    # Count signal categories
    category_counts = {}
    for segment in fls_segments:
        for category in segment['signal_words'].keys():
            category_counts[category] = category_counts.get(category, 0) + 1

    return {
        'section': section_name,
        'total_fls_found': total_segments,
        'average_fls_score': round(avg_score, 3),
        'signal_categories': category_counts,
        'fls_segments': fls_segments[:50],  # Limit to top 50
        'metadata': {
            'text_length': len(text),
            'total_sentences': len(re.split(r'(?<=[.!?])\s+', text)),
            'fls_density': round(total_segments / len(re.split(r'(?<=[.!?])\s+', text)), 3) if text else 0.0
        }
    }


def extract_fls_from_10k_section(
    section_text: str,
    section_number: str,
    section_name: str
) -> str:
    """
    Tool function: Extract FLS from a 10-K section.

    This function is designed to be used as an Agent Framework tool.

    Args:
        section_text: Full text of the 10-K section
        section_number: Section number (e.g., "7", "1A")
        section_name: Section name (e.g., "MD&A", "Risk Factors")

    Returns:
        JSON string with FLS analysis results
    """
    section_label = f"Section {section_number} - {section_name}"
    analysis = analyze_fls_in_text(section_text, section_label)

    return json.dumps(analysis, indent=2)


def classify_fls_category_mda(text: str) -> str:
    """
    Classify FLS category for MD&A section.

    Categories:
    - revenue_guidance: Revenue/earnings projections
    - strategic: Strategic initiatives and plans
    - market_outlook: Market expectations
    - operational: Operational improvements
    - capital: Capital allocation plans
    - risk_mitigation: Risk mitigation strategies

    Args:
        text: FLS text to classify

    Returns:
        Category name
    """
    text_lower = text.lower()

    # Revenue/Earnings indicators
    if any(word in text_lower for word in ['revenue', 'earnings', 'sales', 'profitability', 'margin', 'guidance']):
        return 'revenue_guidance'

    # Strategic indicators
    if any(word in text_lower for word in ['expand', 'acquisition', 'growth', 'strategy', 'initiative', 'launch']):
        return 'strategic'

    # Market outlook indicators
    if any(word in text_lower for word in ['market', 'demand', 'competition', 'industry', 'sector']):
        return 'market_outlook'

    # Capital allocation indicators
    if any(word in text_lower for word in ['invest', 'dividend', 'buyback', 'capital', 'spending', 'capex']):
        return 'capital'

    # Risk mitigation indicators
    if any(word in text_lower for word in ['mitigate', 'manage risk', 'hedge', 'diversify']):
        return 'risk_mitigation'

    # Operational indicators
    if any(word in text_lower for word in ['operation', 'efficiency', 'productivity', 'manufacturing', 'supply chain']):
        return 'operational'

    return 'other'


def classify_fls_category_risk(text: str) -> str:
    """
    Classify FLS category for Risk Factors section.

    Categories:
    - market: Market and competitive risks
    - operational: Operational risks
    - financial: Financial risks
    - regulatory: Regulatory and legal risks
    - strategic: Strategic execution risks
    - external: External/geopolitical risks

    Args:
        text: FLS text to classify

    Returns:
        Category name
    """
    text_lower = text.lower()

    # Market risk indicators
    if any(word in text_lower for word in ['competition', 'market share', 'demand', 'pricing']):
        return 'market'

    # Regulatory risk indicators
    if any(word in text_lower for word in ['regulat', 'compliance', 'legal', 'litigation', 'law']):
        return 'regulatory'

    # Financial risk indicators
    if any(word in text_lower for word in ['interest rate', 'credit', 'liquidity', 'debt', 'financial']):
        return 'financial'

    # External risk indicators
    if any(word in text_lower for word in ['geopolitical', 'economic', 'pandemic', 'climate', 'political']):
        return 'external'

    # Strategic risk indicators
    if any(word in text_lower for word in ['strategy', 'execution', 'innovation', 'technology']):
        return 'strategic'

    # Operational risk indicators
    if any(word in text_lower for word in ['operation', 'supply chain', 'manufacturing', 'disruption']):
        return 'operational'

    return 'other'


# Export toolkit functions
def get_fls_detection_tools() -> List[callable]:
    """
    Get list of FLS detection tools for Agent Framework.

    Returns:
        List of tool functions
    """
    return [
        extract_fls_from_10k_section,
        detect_fls_signal_words,
        calculate_fls_score,
        classify_fls_category_mda,
        classify_fls_category_risk,
    ]
