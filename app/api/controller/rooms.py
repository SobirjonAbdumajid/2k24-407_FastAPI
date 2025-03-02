from fastapi import Depends, HTTPException
from starlette import status

from app.api.repositories.rooms import RoomsRepository


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
