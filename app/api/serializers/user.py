from typing import Mapping

from app.api.schemas.auth import User


class UserSerializer:
    def serialize(self, data: Mapping) -> User:
        return User.model_validate(data)
