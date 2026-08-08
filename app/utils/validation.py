import re

KEYWORDS = ["market", "competition", "profit", "growth", "user", "engagement", "revenue"]

def heuristic_score(description: str) -> float:
    """Return a score between 0 and 100 based on keyword presence and length."""
    if not description:
        return 0.0
    desc = description.lower()
    keyword_hits = sum(1 for kw in KEYWORDS if kw in desc)
    length_factor = min(len(desc.split()), 100) / 100
    score = (keyword_hits / len(KEYWORDS)) * 70 + length_factor * 30
    return round(min(score, 100), 2)
