import random
from typing import List, Tuple

class AIStub:
    def generate_validation(self, description: str, tags: List[str]) -> Tuple[float, str, List[str]]:
        # Deterministic mock: score based on length, random features
        score = min(1.0, len(description) / 500)
        text = f"Your idea scores {score:.2f} based on preliminary analysis."
        features = [f"Feature {i}" for i in range(1, 4)]
        return score, text, features

    def generate_mvp_code(self, idea_id: str, features: List[str]) -> str:
        # Return a simple Python FastAPI skeleton
        code = """from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'message': 'Hello from MVP'}\n"""
        return code
