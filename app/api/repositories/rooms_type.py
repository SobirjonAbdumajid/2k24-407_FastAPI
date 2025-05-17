from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from app.api.schemas.rooms_type import RoomTypeResponseSchema, RoomTypeCreateOrUpdateSchema
from app.api.models.rooms import RoomsType

from app.core.database.config import get_general_session


class RoomTypeRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_rooms_types(self) -> Sequence[RoomTypeResponseSchema]:
        result = await self.__session.execute(select(RoomsType))
        return [RoomTypeResponseSchema.model_validate(rt) for rt in result.scalars().all()]

    async def get_rooms_type_by_id(self, room_type_id: int) -> RoomsType | None:
        return await self.__session.get(RoomsType, room_type_id)

    async def _get_rooms_type_by_title(self, title: str) -> bool:
        result = await self.__session.execute(select(RoomsType).where(RoomsType.title.ilike(f"%{title}%")))
        return bool(result.scalars().first())

    async def create_rooms_type(self, room_type: RoomTypeCreateOrUpdateSchema) -> RoomTypeResponseSchema:
        if await self._get_rooms_type_by_title(room_type.title):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room type already exists")

        new_room_type = RoomsType(**room_type.model_dump())
        self.__session.add(new_room_type)
        await self.__session.commit()
        await self.__session.refresh(new_room_type)
        return RoomTypeResponseSchema.model_validate(new_room_type)

    async def update_rooms_type(self, room_type_id: int, data: RoomTypeCreateOrUpdateSchema) -> RoomTypeResponseSchema:
        room_type = await self.get_rooms_type_by_id(room_type_id)
        if room_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found")
        if await self._get_rooms_type_by_title(data.title):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room type already exists")
        room_type.title = data.title
        await self.__session.commit()
        await self.__session.refresh(room_type)
        return RoomTypeResponseSchema.model_validate(room_type)

    async def delete_rooms_type(self, room_type_id: int) -> None:
        room_type = await self.get_rooms_type_by_id(room_type_id)
        if room_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found")
        await self.__session.delete(room_type)
        await self.__session.commit()
        return None

