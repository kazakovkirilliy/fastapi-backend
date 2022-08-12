
from uuid import UUID
from pydantic import BaseModel


# 0 -> unlike
# 1 -> like
class Participation(BaseModel):
    post_id: UUID
