from fastapi import APIRouter, Query
from . import schemas
from .controllers import StreamController
from typing import Optional

router = APIRouter(prefix="/v1/stream", tags=["Stream"])
controller = StreamController()


@router.post("/create", status_code=201, responses={
                201: {"model": schemas.StreamResponse, "description": "Create items success"}})
async def create_stream(data: schemas.StreamCreate):
    result = await controller.create(data.model_dump())
    return schemas.StreamResponse(**result)


@router.get("/get/{stream_id}", status_code=200, responses={
                200: {"model": schemas.StreamResponse, "description": "Get items success"}})
async def get_stream(stream_id: str):
    result = await controller.get(stream_id)
    return result


@router.put("/edit/{stream_id}", status_code=200, responses={
                200: {"model": schemas.StreamResponse, "description": "Edit items success"}})
async def update_stream(stream_id: str, data: schemas.StreamUpdate):
    result = await controller.update(stream_id, data.model_dump(exclude_unset=True))
    return schemas.StreamResponse(**result)


@router.delete("/delete/{steam_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_stream(stream_id: str):
    result = await controller.delete(stream_id)
    return result


@router.get("/search", status_code=200, responses={
                200: {"model": schemas.PaginatedStreamResponse, "description": "Get items success"}})
async def list_stream(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search by title or genre"),
):
    query = {}
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"genre": {"$regex": search, "$options": "i"}},
        ]
    result = await controller.search(query, page, limit)
    return result

"""
@router.get("/playlist/{stream_id}", status_code=200, responses={
                200: {"model": schemas.PlayListResponse, "description": "Get items success"}
})
async def play_list(stream_id: str):
    result = await controller.play_list(stream_id)
    return schemas.PlayListResponse(**result)


@router.get("/playvideo/{stream_id}", response_class=PlainTextResponse, responses={
                200: {"description": "Play items success"}
})
async def play_video(stream_id: str, resolution: Optional[str] = Query("auto", description="auto| 360x640 | 480x854 | 720x1280 | 1080x1920")):
    result = await controller.play_video(stream_id, resolution)
    return PlainTextResponse(result, media_type="application/vnd.apple.mpegurl")
"""