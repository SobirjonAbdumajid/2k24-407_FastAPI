from fastapi import Depends, HTTPException
from typing import Sequence

from app.api.schemas.rooms_type import RoomTypeResponseSchema, RoomTypeCreateOrUpdateSchema
from app.api.repositories.rooms_type import RoomTypeRepository


class RoomTypeController:
    def __init__(self,
                 room_type_repository: RoomTypeRepository = Depends(),
                 ):
        self.__room_type_repository = room_type_repository

    async def get_rooms_types(self) -> Sequence[RoomTypeResponseSchema]:
        return await self.__room_type_repository.get_rooms_types()

    async def get_rooms_type(self, room_type_id: int) -> RoomTypeResponseSchema:
        res = await self.__room_type_repository.get_rooms_type_by_id(room_type_id)
        if not res:
            raise HTTPException(status_code=404, detail="Room type not found")
        return RoomTypeResponseSchema.model_validate(res)

    async def create_rooms_type(self, room_type: RoomTypeCreateOrUpdateSchema) -> RoomTypeResponseSchema:
        return await self.__room_type_repository.create_rooms_type(room_type)

    async def update_rooms_type(self, room_type_id, room_type: RoomTypeCreateOrUpdateSchema) -> RoomTypeResponseSchema:
        return await self.__room_type_repository.update_rooms_type(room_type_id, room_type)

    async def delete_rooms_type(self, room_type_id) -> None:
        return await self.__room_type_repository.delete_rooms_type(room_type_id)
