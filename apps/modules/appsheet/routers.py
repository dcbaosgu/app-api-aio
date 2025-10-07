from fastapi import APIRouter
from .schemas import ReportRequest
from .controllers import AppSheetController


router = APIRouter(prefix="/v1/appsheet", tags=["AppSheet"])
controller = AppSheetController()


@router.post("/send-report", status_code=200, responses={
                200: {"description": "Post items success"}})
async def send_report(data: ReportRequest):
    result =  await controller.send_report(data.dict())
    return result

@router.get("/fetch-report", status_code=200, responses={
                200: {"description": "Fetch items success"}})
async def fetch_report(page: int = 1, limit: int = 10):
    result = await controller.fetch_report(page, limit)
    return result