
from app.api.schemas.token import TokenData


class TokenSerializer:
    def serialize(self, token: str) -> TokenData:
        return TokenData(
            access_token=token
        )
