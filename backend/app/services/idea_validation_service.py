import os
import httpx
from fastapi import HTTPException
from app.utils.exceptions import ExternalAPIError

EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://api.example.com/validate")
EXTERNAL_API_TIMEOUT = 5.0

async def validate_idea(description: str) -> float:
    async with httpx.AsyncClient(timeout=EXTERNAL_API_TIMEOUT) as client:
        try:
            response = await client.post(EXTERNAL_API_URL, json={"description": description})
            response.raise_for_status()
            data = response.json()
            score = float(data.get("validation_score"))
            if not (0 <= score <= 100):
                raise ValueError("Score out of bounds")
            return score
        except httpx.HTTPStatusError as exc:
            raise ExternalAPIError(f"External API error: {exc}") from exc
        except httpx.RequestError as exc:
            raise ExternalAPIError(f"Request error: {exc}") from exc
        except (ValueError, KeyError) as exc:
            raise ExternalAPIError(f"Invalid response: {exc}") from exc