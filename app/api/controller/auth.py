from datetime import timedelta

from passlib.hash import bcrypt

from fastapi import Depends, HTTPException, status
from jose import jwt, ExpiredSignatureError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.repositories.auth import AuthRepository
from app.api.schemas.auth import UserInSchema
from app.api.serializers.token import TokenSerializer
from app.api.utils.auth import check_password
from app.api.utils.auth import create_access_token
from app.core.settings import get_settings, Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthController:
    def __init__(
            self,
            settings: Settings = Depends(get_settings),
            auth_repo: AuthRepository = Depends(),
            token_serializer: TokenSerializer = Depends()
    ):
        self.settings = settings
        self.auth_repo = auth_repo
        self.token_serializer = token_serializer

    async def create_user(self, data: UserInSchema) -> None:
        data.password = bcrypt.hash(data.password)
        return await self.auth_repo.create_user(data=data.model_dump())

    async def check_user(self, data: OAuth2PasswordRequestForm) -> bool:
        user = await self.auth_repo.get_user_if_exists(username=data.username)
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
        return self.token_serializer.serialize(
            create_access_token(
                user.model_dump(exclude={"id", "password"}),
                expires_delta=timedelta(seconds=self.settings.JWT_EXPIRE_SECONDS)
            )
        )

    async def get_current_user(
            self,
            token: str
    ):
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCRYPT_ALGORITHM]
            )
            user = await self.auth_repo.get_user_if_exists(payload.get("username"))
            return user
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Expired token')
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
