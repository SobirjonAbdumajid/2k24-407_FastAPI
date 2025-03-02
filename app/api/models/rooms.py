from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    room_number: Mapped[int]
    room_type: Mapped[int] = mapped_column(ForeignKey('rooms_type.id'))
    price: Mapped[float]
    status: Mapped[int] = mapped_column(ForeignKey('rooms_status.id'))


class RoomsType(Base):
    __tablename__ = 'rooms_type'

    title: Mapped[str]


class RoomsStatus(Base):
    __tablename__ = 'rooms_status'

    title: Mapped[str]
