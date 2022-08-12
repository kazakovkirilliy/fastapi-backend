from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Access Token Response
    """

    access_token: str
    token_type: str
    # expires_in: int
    # scope: str
    # refresh_token: str | None


class TokenData(BaseModel):
    user_id: Optional[str]
