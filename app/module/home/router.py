from typing import Optional
from fastapi import APIRouter, Query
from .exception import ErrorCode
from .controller import HomeController

router = APIRouter(prefix="/v1/home", tags=["Home"])
controller = HomeController()


@router.get("/ping", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def home():
    result = {"ping":"pong"}
    return result


@router.get("/db/backup", status_code=200, responses={
                200: {"description": "Get items success"}})
async def backup_db():
    try:
        return await controller.backup_db()
    except Exception as e:
        print("[HOME] Error backup data:", e)
        raise ErrorCode.BackupDatabaseFailed()
    

@router.get("/log/tracking", status_code=200, responses={
                200: {"description": "Get items success"}})
async def list_loggings(
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(10, le=100, description="Quantity items per page"),
    user_id: Optional[str] = Query(None, description="Filter User ID"),
    start_time: Optional[str] = Query(None, description="Start time (Format: DD-MM-YYYY HH:MM:SS)-GMT+7"),
    end_time: Optional[str] = Query(None, description="End time (Format: DD-MM-YYYY HH:MM:SS)-GMT+7)")
):
    query = {}
    if user_id: query["user_id"] = user_id
    
    result = await controller.search(query, page, limit, start_time, end_time)
    return result
