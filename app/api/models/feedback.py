from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class FeedBack(Base):
    __tablename__ = 'feedback'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="SET NULL"))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"))
    comment: Mapped[str]
