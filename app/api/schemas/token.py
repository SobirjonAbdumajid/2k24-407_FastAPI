from pydantic import BaseModel


class TokenData(BaseModel):
    access_token: str
    token_type: str | None = "bearer"
