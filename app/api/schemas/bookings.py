from pydantic import BaseModel
from datetime import date


class BookingSchema(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date
    status: str
