from pydantic import BaseModel, ConfigDict


class RoomTypeResponseSchema(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class RoomTypeCreateOrUpdateSchema(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)
