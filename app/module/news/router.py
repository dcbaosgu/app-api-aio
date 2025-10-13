from fastapi import APIRouter, Query
from . import schema
from .controller import RSSController

router = APIRouter(prefix="/v1/rss", tags=["RSS"])
controller = RSSController()

@router.get("/news", status_code=200, responses={
            200: {"model": schema.PaginatedRSSResponse, "description": "Get items success"}
})
async def list_rss(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    category: str = Query(..., enum=["kinh-doanh.rss", "khoa-hoc-cong-nghe.rss", "giai-tri.rss"]),
    search: str = Query(None, description="Search by title")
):
    result = await controller.list_rss(page, limit, category, search)
    return result
