from fastapi import APIRouter, Depends, status
from app.api.controller.booking import BookingController
from app.api.dependecies.get_current_user import get_user
from app.api.schemas.bookings import BookingSchema

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED)
async def make_booking(
        booking: BookingSchema,
        controller: BookingController = Depends()
):
    return await controller.make_booking(booking)
