import os
import logging
import openai
from typing import List, Tuple

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    pass

class ValidationService:
    def __init__(self, openai_api_key: str = None, timeout: int = 30):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        openai.api_key = self.api_key
        self.timeout = timeout

    def validate_idea(self, description: str, tags: List[str]) -> Tuple[float, str, List[str]]:
        prompt = (
            f"Validate the following business idea:\n\n"
            f"Description: {description}\n"
            f"Industry Tags: {', '.join(tags)}\n\n"
            f"Return a JSON object with keys: score (0-100), text (validation explanation), "
            f"features (list of 3 recommended MVP features)."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a product validation assistant."},
                          {"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=512,
                timeout=self.timeout,
            )
            content = response.choices[0].message.content
            data = self._parse_response(content)
            return data["score"], data["text"], data["features"]
        except openai.OpenAIError as e:
            logger.exception("OpenAI API error during validation")
            raise ValidationError(f"OpenAI validation failed: {e}") from e
        except Exception as e:
            logger.exception("Unexpected error during validation")
            raise ValidationError(f"Unexpected validation error: {e}") from e

    def _parse_response(self, content: str) -> dict:
        import json
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValidationError("OpenAI response is not valid JSON")
        if not all(k in data for k in ("score", "text", "features")):
            raise ValidationError("OpenAI response missing required keys")
        if not isinstance(data["features"], list) or len(data["features"]) < 3:
            raise ValidationError("OpenAI response features list is insufficient")
        return data