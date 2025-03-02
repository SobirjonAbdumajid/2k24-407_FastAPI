from pydantic import BaseModel


class RoomsSchema(BaseModel):
    room_number: int
    room_type: str
    price: float
    status: str
