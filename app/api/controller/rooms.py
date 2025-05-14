from fastapi import Depends

from app.api.repositories.rooms import RoomsRepository
from app.api.schemas.rooms import RoomsCreateSchema
from app.api.tasks.rooms import update_creating_rooms


class RoomsController:
    def __init__(
            self,
            rooms_repo: RoomsRepository = Depends()
    ):
        self.__rooms_repo = rooms_repo

    async def get_rooms(self):
        return await self.__rooms_repo.get_all_rooms()

    async def get_room(self, room_id):
        items = await self.__rooms_repo.get_room(room_id=room_id)
        # if not items or None:
        #     raise HTTPException(
        #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #         detail={
        #             "message": "Row does not exist"
        #         }
        #     )
        return items

    async def create_room(self, body: RoomsCreateSchema):
        celery_tasks_id = await self.__rooms_repo.create_room(
            room_number=body.room_number,
            room_type=body.room_type,
            price=body.price,
            status=body.status
        )
        update_creating_rooms.delay(task_id=str(celery_tasks_id))
        return celery_tasks_id
