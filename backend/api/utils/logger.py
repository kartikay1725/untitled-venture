import logging
import uuid
from fastapi import Request

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = getattr(record, "correlation_id", "unknown")
        return True

def get_logger(name: str = "ideaforge"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s","correlation_id":"%(correlation_id)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.addFilter(CorrelationIdFilter())
    return logger

async def add_correlation_id(request: Request, call_next):
    request.state.correlation_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = request.state.correlation_id
    return response