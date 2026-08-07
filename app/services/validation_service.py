import asyncio
from typing import List, Tuple

class ValidationService:
    async def validate(self, description: str, tags: List[str]) -> Tuple[float, str, List[str]]:
        await asyncio.sleep(0.1)
        word_count = len(description.split())
        score = min(1.0, max(0.0, word_count / 200))
        text = f"Score based on description length ({word_count} words)."
        features = [f"Feature {i+1}" for i in range(min(3, len(tags)))]
        return score, text, features
