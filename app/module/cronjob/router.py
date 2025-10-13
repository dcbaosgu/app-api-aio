from fastapi import APIRouter, Query
from . import schema
from .controller import CronController
from typing import Optional


router = APIRouter(prefix="/v1/cronjob", tags=["Cronjob"])
controller = CronController()


@router.post("/create", status_code=201, responses={
                201: {"model": schema.CronResponse, "description": "Create items success"}})
async def create_cron(data: schema.CronCreate):
    result = await controller.create(data.model_dump())
    return schema.CronResponse(**result)

@router.get("/getdb/{cron_id}", status_code=200, responses={
                200: {"model": schema.CronResponse, "description": "Get items success"}})
async def get_db(cron_id: str):
    result = await controller.getdb(cron_id)
    return result

@router.get("/runtime", status_code=200, responses={
                200: {"model": schema.CronRuntimeResponse, "description": "Fetch items success"}
            })
async def runtime():
    result = await controller.runtime()
    return result

@router.put("/edit/{cron_id}", status_code=200, responses={
                200: {"model": schema.CronResponse, "description": "Edit items success"}})
async def update_cron(cron_id: str, data: schema.CronUpdate):
    result = await controller.update(cron_id, data.model_dump(exclude_unset=True))
    return schema.CronResponse(**result)

@router.delete("/delete/{cron_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_cron(cron_id: str):
    result = await controller.delete(cron_id)
    return result


@router.get("/search", status_code=200, responses={
                200: {"model": schema.PaginatedCronResponse, "description": "Get items success"}})
async def list_cron(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
):
    query = {}
    if search:
        query["$or"] = [
            {"task": {"$regex": search, "$options": "i"}},
            {"endpoint": {"$regex": search, "$options": "i"}},
        ]
    result = await controller.search(query, page, limit)
    return result
