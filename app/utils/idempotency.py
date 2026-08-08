import time
from typing import Dict

class IdempotencyStore:
    def __init__(self, ttl_seconds: int = 3600):
        self.store: Dict[str, dict] = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> dict | None:
        entry = self.store.get(key)
        if entry and entry["expires_at"] > time.time():
            return entry["value"]
        self.store.pop(key, None)
        return None

    def set(self, key: str, value: dict):
        self.store[key] = {"value": value, "expires_at": time.time() + self.ttl}