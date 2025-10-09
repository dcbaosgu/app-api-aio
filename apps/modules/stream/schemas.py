from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class StreamCreate(BaseModel):
    title: str
    genre: Literal["tutorial", "relax", "other"]
    tags: Optional[List[str]] = None
    path: str
    ratio: Literal["vertical", "horizontal"] = "horizontal"
    desc: Optional[str] = None
    access_role: Literal["public", "private", "business"] = "public"
    allow_id: Optional[List[str]] = None
    viewer: int = 0
    upload_by: str


class StreamUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[Literal["tutorial", "relax", "other"]] = None
    tags: Optional[List[str]] = None
    path: Optional[str] = None
    ratio: Optional[str] = None
    desc: Optional[str] = None
    access_role: Optional[Literal["public", "private", "business"]] = None
    allow_id: Optional[List[str]] = None
    # viewer: Optional[int] = None
    # upload_by: Optional[str] = None


class StreamResponse(BaseModel):
    id: str = Field(alias="_id")
    title: Optional[str]
    genre: Optional[str]
    tags: Optional[List[str]] = None
    path: Optional[str]
    ratio: Optional[str]
    desc: Optional[str] = None
    access_role: Optional[str]
    allow_id: Optional[List[str]] = None
    viewer: Optional[int]
    upload_by: Optional[str]
    created_at: Optional[float]
    updated_at: Optional[float] = None


class PaginatedStreamResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[StreamResponse]


class ResolutionItem(BaseModel):
    bandwidth: int
    resolution: str
    path: str


class PlayListResponse(BaseModel):
    stream_id: str
    ratio: str
    resolutions: List[ResolutionItem]