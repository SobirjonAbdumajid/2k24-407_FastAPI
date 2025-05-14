import asyncio

from celery import shared_task

from app.api.repositories.rooms import RoomsRepository
from app.core.database.config import get_general_sync_session


def do_something_sync(task_id: str):
    with get_general_sync_session() as session:
        repo = RoomsRepository(sync_session=session)
        repo.update_room(task_id)


@shared_task
def update_creating_rooms(task_id: str):
    print("PROCESS STARTING")
    do_something_sync(task_id)
    print("ALL SUCCESS")
