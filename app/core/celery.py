from celery import Celery

from app.core.settings import get_settings

settings = get_settings()

celery = Celery(
    "celery_worker",
    broker=settings.GET_REDIS_URL,
    backend=settings.GET_REDIS_URL,
    include=["app.api.tasks"]
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)
