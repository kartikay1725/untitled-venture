import time
import logging
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from prometheus_client import Histogram

request_latency = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'])

class LatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        latency = time.time() - start_time
        request_latency.labels(request.method, request.url.path).observe(latency)
        return response