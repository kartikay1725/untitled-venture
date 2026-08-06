import asyncio

def _simulate_validation(idea_id: str):
    # Dummy deterministic logic
    return {
        "score": 0.85,
        "feedback": {"feasibility": "High", "market_need": "Moderate"},
    }

async def validate_idea(idea_id: str):
    await asyncio.sleep(1)  # Simulate network latency
    return _simulate_validation(idea_id)
