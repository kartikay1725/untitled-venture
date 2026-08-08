"""Heuristic idea validation.

The function returns a score between 0 and 100 based on simple keyword checks.
"""

import re

KEYWORDS = ["market", "problem", "solution", "value", "customer"]
MIN_WORDS = 10

def validate_idea(description: str) -> float:
    words = re.findall(r"\w+", description.lower())
    if len(words) < MIN_WORDS:
        return 40.0
    keyword_hits = sum(1 for kw in KEYWORDS if kw in description.lower())
    score = 50 + (keyword_hits / len(KEYWORDS)) * 50
    return round(min(max(score, 0), 100), 2)