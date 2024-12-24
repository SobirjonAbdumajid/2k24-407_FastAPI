from fastapi import Depends
from app.api.repositories.booking import BookingRepository
from app.api.schemas.bookings import BookingSchema


class BookingController:
    def __init__(
            self,
            booking_repo: BookingRepository = Depends(),
    ):
        self.__booking_repo = booking_repo

    async def make_booking(self, data: BookingSchema):
        day = (data.check_out - data.check_in).days
        room_price = await self.__booking_repo.get_room_price(data.room_id)
        total_price = day * room_price
        return await self.__booking_repo.make_booking(data, total_price)
