from celery import Celery

from app.core.settings import get_settings

settings = get_settings()

celery = Celery(
    "celery_worker",
    broker=settings.GET_REDIS_URL,
    backend=settings.GET_REDIS_URL,
)
