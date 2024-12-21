from passlib.hash import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.repositories.auth import AuthRepository
from app.api.schemas.auth import UserInSchema
from app.api.utils.auth import check_password


class AuthController:
    def __init__(
            self,
            auth_repo: AuthRepository = Depends(),
            token_serializer: TokenSerializer = Depends()
    ):
        self.auth_repo = auth_repo

    async def create_user(self, data: UserInSchema) -> None:
        data.password = bcrypt.hash(data.password)
        return await self.auth_repo.create_user(data=data.model_dump())

    async def check_user(self, data: OAuth2PasswordRequestForm) -> bool:
        user = self.auth_repo.check_exist_user(username=data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not Authorized'
            )
        if not check_password(user.password, data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not Authorized'
            )
