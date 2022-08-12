
from uuid import UUID
from pydantic import BaseModel


# 0 -> unlike
# 1 -> like
class Like(BaseModel):
    post_id: UUID
