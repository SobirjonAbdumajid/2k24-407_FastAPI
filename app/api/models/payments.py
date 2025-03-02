from datetime import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class Payments(Base):
    __tablename__ = "payments"

    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="SET NULL"))
    payment_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    amount: Mapped[float]
    payment_method: Mapped[str]
    status: Mapped[str]
