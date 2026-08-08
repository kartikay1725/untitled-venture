import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.utils.settings import Settings

settings = Settings()
client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

async def upload_file(key: str, data: bytes, content_type: str) -> str:
    try:
        client.put_object(Bucket=settings.S3_BUCKET_NAME, Key=key, Body=data, ContentType=content_type)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError("S3 upload failed") from exc
    return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{key}"