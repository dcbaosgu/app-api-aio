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

@router.get("/get-report", status_code=200,
            responses={200: {"description": "Get report success"}})
async def get_report(page: int = 1, limit: int = 10):
    return await controller.get_report(page, limit)