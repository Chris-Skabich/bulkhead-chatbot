import os
from celery import Celery

# Securely pull the Redis URL from the environment
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "bulkhead_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)