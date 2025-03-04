from fastapi import Depends, APIRouter, status
from typing import Sequence

from app.api.controller.rooms_type import RoomTypeController
from app.api.schemas.rooms_type import RoomTypeResponseSchema, RoomTypeCreateOrUpdateSchema

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[RoomTypeResponseSchema],
)
async def get_rooms_types(
        controller: RoomTypeController = Depends()
):
    return await controller.get_rooms_types()


@router.get(
    "/{room_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoomTypeResponseSchema,
)
async def get_rooms_type(
        room_id: int,
        controller: RoomTypeController = Depends()
):
    return await controller.get_rooms_type(room_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoomTypeCreateOrUpdateSchema,
)
async def create_rooms_type(
        room_type: RoomTypeCreateOrUpdateSchema,
        controller: RoomTypeController = Depends()
):
    return await controller.create_rooms_type(room_type)


@router.put(
    "/{room_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoomTypeResponseSchema,

)
async def update_rooms_type(
        room_id: int,
        room_type: RoomTypeCreateOrUpdateSchema,
        controller: RoomTypeController = Depends()
):
    return await controller.update_rooms_type(room_id, room_type)


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_rooms_type(
        room_id: int,
        controller: RoomTypeController = Depends()
) -> None:
    return await controller.delete_rooms_type(room_id)
