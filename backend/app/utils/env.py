import os
from typing import List

# Required env vars
REQUIRED_VARS = [
    "DATABASE_URL",
    "JWT_SECRET",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "S3_BUCKET_NAME",
    "ALLOWED_ORIGINS",
]

def validate_required_vars():
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

# CORS origins
ORIGINS: List[str] = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",") if origin.strip()]