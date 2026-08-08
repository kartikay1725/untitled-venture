import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import asyncio
import logging

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

async def upload_file_to_s3(file_bytes: bytes, key: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _upload_sync, file_bytes, key)

def _upload_sync(file_bytes: bytes, key: str) -> str:
    s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=file_bytes)
    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
