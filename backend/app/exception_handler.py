from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .utils.logger import logger

def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTP error", status=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": str(exc.status_code), "message": exc.detail, "details": {}}}
    )