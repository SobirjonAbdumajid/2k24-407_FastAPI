from pydantic import BaseModel


class RoomsSchema(BaseModel):
    room_number: int
    room_type: str
    price: float
    status: str


class RoomsCreateSchema(BaseModel):
    room_number: int
    room_type: int
    price: float
    status: int
