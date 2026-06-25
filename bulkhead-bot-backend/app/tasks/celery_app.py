import os
from celery import Celery

# Securely pull the Redis URL from the environment
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

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

# Now lets test connection
@celery_app.task(name="test_celery_connection")
def test_task(name: str):
    message = f"Success! Celery is processing a background task for {name}"
    print(message)  # This will print inside your Celery Docker terminal logs
    return message