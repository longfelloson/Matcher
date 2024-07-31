from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from config import settings
from logger import logger


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_name: str, file: bytes):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name, Key=file_name, Body=file, ACL="public-read"
                )
        except ClientError as e:
            logger.error("Error uploading file via S3: %s", e)

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            logger.error("Error deleting file via S3: %s", e)

    async def update_file(self, file: bytes, file_name: str) -> None:
        """
        Перезапись файла
        """
        await self.delete_file(file_name)
        await self.upload_file(file_name, file)

    def get_file_url(self, file_name: str, extension: str = "jpg") -> str:
        return (
            f"{self.config['endpoint_url']}/{self.bucket_name}/{file_name}.{extension}"
        )


s3_client = S3Client(
    access_key=settings.S3.S3_ACCESS_KEY,
    secret_key=settings.S3.S3_SECRET_KEY,
    endpoint_url=settings.S3.S3_ENDPOINT_URL,
    bucket_name=settings.S3.S3_BUCKET_NAME,
)
