import os
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Optional

class FileStorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.bucket = os.getenv("S3_BUCKET_NAME")
        if not self.bucket:
            raise ValueError("S3_BUCKET_NAME not set")

    def upload_file(self, file_bytes: bytes, key: str, content_type: str) -> str:
        try:
            self.s3.put_object(Bucket=self.bucket, Key=key, Body=file_bytes, ContentType=content_type)
            return f"https://{self.bucket}.s3.amazonaws.com/{key}"
        except ClientError as e:
            logging.error(f"S3 upload failed: {e}")
            raise

    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as e:
            logging.error(f"Presigned URL generation failed: {e}")
            raise