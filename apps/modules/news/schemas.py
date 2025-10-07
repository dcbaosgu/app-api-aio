from typing import List
from pydantic import BaseModel


class RSSResponse(BaseModel):
    title: str
    link: str
    image: str
    description: str
    created_at: str


class PaginatedRSSResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[RSSResponse]
