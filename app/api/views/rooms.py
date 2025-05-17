from fastapi import APIRouter, Depends

from app.api.controller.rooms import RoomsController
from app.api.schemas.rooms import RoomsCreateSchema

router = APIRouter()


@router.get(
    ""
)
async def get_rooms(
        controller: RoomsController = Depends()
):
    return await controller.get_rooms()


@router.get("/{room_id}/")
async def get_room(
        room_id: int,
        controller: RoomsController = Depends()
):
    return await controller.get_room(room_id=room_id)


@router.post(
    "/",
)
async def save_room(
        payload: RoomsCreateSchema,
        controller: RoomsController = Depends()
):
    return await controller.create_room(body=payload)
