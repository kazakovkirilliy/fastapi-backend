from typing import Optional
from fastapi import Query
from pydantic import BaseModel
from typing import Literal


SortDirection = Literal["asc", "desc"]


class ResponsePager(BaseModel):
    """
    Response wrapper for pageable data.
    """

    content: list
    offset: int
    limit: int
    count: int
    total_count: int
    order: list[SortDirection]
    order_by: list[str]
    search: str


class RequestPager:
    def __init__(
        self,
        search: Optional[str] = Query("", description="Search value"),
        offset: Optional[int] = Query(0, description="Paging start"),
        limit: Optional[int] = Query(15, description="Page size"),
        order_by: Optional[list[str]] = Query(
            [], description="List of field ordering"),
        order: Optional[list[SortDirection]] = Query(
            [], description="Order direction. Must match order_by param."
        ),
    ) -> None:
        self.offset = offset
        self.limit = limit
        self.order_by = order_by
        self.order = order
        self.search = search
