import asyncio
from typing import Tuple, Dict

async def validate_idea(title: str, description: str) -> Tuple[float, Dict]:
    await asyncio.sleep(2)
    score = min(100, len(title) * 2 + len(description) * 0.5)
    feedback = {"feasibility": "High", "market_need": "Moderate"}
    return score, feedback
