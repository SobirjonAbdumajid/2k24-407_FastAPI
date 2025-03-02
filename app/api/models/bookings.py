from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"))
    check_in: Mapped[datetime]
    check_out: Mapped[datetime]
    total_price: Mapped[float]
    status: Mapped[str]
