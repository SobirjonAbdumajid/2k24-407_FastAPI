from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.config import get_general_session


class AuthRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.session = session

    async def create_user(self, data: dict) -> None:
        stmt = text(
            "insert into users(username, password, first_name, last_name, email, is_staff, is_active, is_superuser) "
            "values (:username, :password, :first_name, :last_name, :email, :is_staff, :is_active, :is_superuser)").bindparams(
            **data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def check_exist_user(self, username: str) -> bool:
        pass
