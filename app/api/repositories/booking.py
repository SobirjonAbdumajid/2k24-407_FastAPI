from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database.config import get_general_session
from app.api.models.bookings import Bookings
from app.api.schemas.bookings import BookingSchema


class BookingRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def make_booking(self, data: BookingSchema, total_price: int):
        booking = Bookings(room_id=data.room_id, user_id=data.user_id,
                           check_in=data.check_in, check_out=data.check_out,
                           total_price=total_price, status=data.status)
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def get_room_price(self, room_id: int):
        stmt = await self.session.execute(text(
            """SELECT price FROM rooms where id=:room_id;"""
        ).bindparams(room_id=room_id))
        return stmt.scalar()
