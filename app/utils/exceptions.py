from fastapi import HTTPException

class ExternalAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=502, detail=detail)
