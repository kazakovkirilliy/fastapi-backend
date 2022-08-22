from typing import Optional
from pydantic import BaseModel


class LocationResponse(BaseModel):
    longitude: float
    latitude: float
    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house_number: Optional[str]

    class Config:
        orm_mode = True
