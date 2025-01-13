import logging
from datetime import datetime, timezone
from io import BytesIO

from mypy_boto3_s3 import S3Client
from PIL import Image
from typing_extensions import override
import time
from os.path import join

from .base import BaseArtifactPublisher

logger: logging.Logger = logging.getLogger(__name__)


def _get_unix_timestamp(now: datetime) -> int:
    return int(time.mktime(now.timetuple()))


class S3ArtifactPublisher(BaseArtifactPublisher):
    def __init__(self, s3: S3Client, bucket_name: str):
        self._s3: S3Client = s3
        self._bucket_name: str = bucket_name

    @staticmethod
    def generate_key(*, subdir: str, now: datetime, run_id: str, seq_no: int, format: str) -> str:
        return join(
            "webrock",
            subdir,
            f"year={now.year}/month={now.month}/day={now.day}/run_id={run_id}/{_get_unix_timestamp(now)}-{seq_no}.{format}",
        )

    @override
    def publish_screenshot(self, *, image: Image.Image, run_id: str, seq_no: int) -> None:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="webp")
        img_bytes = img_byte_arr.getvalue()

        now = datetime.now(timezone.utc)
        key = S3ArtifactPublisher.generate_key(
            subdir="screenshots", now=now, run_id=run_id, seq_no=seq_no, format="webp"
        )
        logger.info(f"Publishing screenshot to bucket '{self._bucket_name}' and key '{key}'")

        resp = self._s3.put_object(Bucket=self._bucket_name, Key=key, Body=img_bytes)
        logger.debug(resp)

    @override
    def publish_system_prompt(self, *, prompt: str, run_id: str, seq_no: int) -> None:
        content_bytes = prompt.encode("utf-8")

        now = datetime.now(timezone.utc)
        key = S3ArtifactPublisher.generate_key(subdir="system", now=now, run_id=run_id, seq_no=seq_no, format="txt")
        logger.info(f"Publishing system prompt to bucket '{self._bucket_name}' and key '{key}'")

        resp = self._s3.put_object(Bucket=self._bucket_name, Key=key, Body=content_bytes)
        logger.debug(resp)

    @override
    def publish_model_response(self, *, response: str, run_id: str, seq_no: int) -> None:
        content_bytes = response.encode("utf-8")

        now = datetime.now(timezone.utc)
        key = S3ArtifactPublisher.generate_key(subdir="responses", now=now, run_id=run_id, seq_no=seq_no, format="txt")
        logger.info(f"Publishing screenshot to bucket '{self._bucket_name}' and key '{key}'")

        resp = self._s3.put_object(Bucket=self._bucket_name, Key=key, Body=content_bytes)
        logger.debug(resp)
