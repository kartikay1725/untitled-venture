import os, json, logging
from typing import List, Dict, Any
import openai
from chromadb import Client as ChromaClient
from chromadb.config import Settings
from pydantic import BaseModel

logger = logging.getLogger("mvpgenie.ai")

class ValidationResult(BaseModel):
    score: float
    feedback: Dict[str, Any]

class BlueprintResult(BaseModel):
    features: List[Dict[str, Any]]
    timeline: Dict[str, Any]

class AIClient:
    def __init__(self, openai_key: str, chroma_url: str):
        openai.api_key = openai_key
        self.chroma = ChromaClient(Settings(chroma_api_impl="chromadb.api.fastapi.FastAPIClient", chroma_server_host=chroma_url.split(":")[0], chroma_server_port=int(chroma_url.split(":")[1])))
        self.collection = self.chroma.get_or_create_collection(name="idea_context")

    async def _retrieve_context(self, query: str, k: int = 5) -> List[str]:
        try:
            results = self.collection.query(query_texts=[query], n_results=k)
            return [doc for doc in results["documents"][0]]
        except Exception as e:
            logger.error(f"Chroma retrieval error: {e}")
            return []

    async def _prompt(self, template: str, variables: Dict[str, Any]) -> str:
        prompt = template.format(**variables)
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1024,
            )
            usage = response.get("usage", {})
            logger.info(f"OpenAI usage: {usage}")
            return response.choices[0].message.content
        except openai.RateLimitError as e:
            logger.warning(f"Rate limit hit: {e}")
            raise
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise

    async def validate_idea(self, title: str, description: str) -> ValidationResult:
        context = await self._retrieve_context(f"{title} {description}")
        template = (
            "You are an expert product analyst. Evaluate the following business idea for feasibility, market fit, and potential risks. "
            "Provide a score between 0 and 1, and detailed feedback. Context: {context}\n\nIdea:\nTitle: {title}\nDescription: {description}\n\nRespond in JSON with keys 'score' and 'feedback'."
        )
        variables = {"context": "\n".join(context), "title": title, "description": description}
        raw = await self._prompt(template, variables)
        try:
            data = json.loads(raw)
            return ValidationResult(score=float(data["score"]), feedback=data["feedback"])
        except Exception as e:
            logger.error(f"Failed to parse validation JSON: {e}")
            raise

    async def generate_blueprint(self, title: str, description: str, scope: str) -> BlueprintResult:
        context = await self._retrieve_context(f"{title} {description}")
        template = (
            "You are a seasoned product manager. For the following idea, generate a prioritized feature list and a timeline for an MVP. "
            "Scope: {scope}. Context: {context}\n\nIdea:\nTitle: {title}\nDescription: {description}\n\nRespond in JSON with keys 'features' (list of objects with 'name' and 'description') and 'timeline' (object with phases)."
        )
        variables = {"context": "\n".join(context), "title": title, "description": description, "scope": scope}
        raw = await self._prompt(template, variables)
        try:
            data = json.loads(raw)
            return BlueprintResult(features=data["features"], timeline=data["timeline"])
        except Exception as e:
            logger.error(f"Failed to parse blueprint JSON: {e}")
            raise
