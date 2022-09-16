from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Access Token Response
    """

    access_token: str
    refresh_token: str | None
    at_exp_time: int
    rt_exp_time: int | None
    # scope: str


class TokenData(BaseModel):
    user_id: Optional[str]
