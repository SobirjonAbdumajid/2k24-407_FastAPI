from pydantic import BaseModel


class RoomTypeResponseSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class RoomTypeCreateOrUpdateSchema(BaseModel):
    title: str

    class Config:
        from_attributes = True
