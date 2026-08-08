class IdeaValidationService:
    @staticmethod
    def validate(description: str) -> float:
        words = description.split()
        score = min(100, max(0, len(words) / 10))
        if "market" in description.lower():
            score += 10
        if "profit" in description.lower():
            score += 10
        return round(score, 2)