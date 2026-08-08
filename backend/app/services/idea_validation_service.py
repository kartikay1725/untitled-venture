import re
from datetime import datetime
import logging

class IdeaValidationService:
    async def validate(self, description: str):
        keywords = ["market", "problem", "solution", "value", "profit"]
        score = 0
        for kw in keywords:
            if re.search(rf"\b{kw}\b", description, re.I):
                score += 20
        length_score = min(len(description) / 200 * 20, 20)
        score += length_score
        score = min(max(score, 0), 100)
        validated_at = datetime.utcnow()
        logging.info(f"Idea validated with score {score}")
        return score, validated_at