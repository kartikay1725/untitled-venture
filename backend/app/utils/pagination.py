from typing import Any, Dict

def cursor_pagination(query, cursor: str | None, limit: int = 20):
    return query.limit(limit)