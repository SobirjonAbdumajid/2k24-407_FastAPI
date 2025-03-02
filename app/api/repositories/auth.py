from fastapi import Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.auth import User
from app.api.serializers.user import UserSerializer
from app.core.database.config import get_general_session


class AuthRepository:
    def __init__(
            self,
            session: AsyncSession = Depends(get_general_session),
            serializer: UserSerializer = Depends()
    ):
        self.session = session
        self.serializer = serializer

    async def create_user(self, data: dict) -> None:
        stmt = text(
            "insert into users(username, password, first_name, last_name, email, is_staff, is_active, is_superuser) "
            "values (:username, :password, :first_name, :last_name, :email, :is_staff, :is_active, :is_superuser)").bindparams(
            **data)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_if_exists(self, username: str) -> User:
        stmt = text("select * from users where username = :username").bindparams(username=username)
        res = await self.session.execute(
            stmt
        )
        mapped_result = res.mappings().first()
        if not mapped_result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
        return self.serializer.serialize(mapped_result)
