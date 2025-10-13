from fastapi import APIRouter
from .controller import SentryController
from . import schema

from worker.sentry.controller import SentryController

router = APIRouter(prefix="/v1/sentry", tags=["Sentry"])
sentry_controller = SentryController()


@router.get("/bug", status_code=500, responses={
                500: {"description": "Test sentry success"}})
async def test_bug():
    result = 1 / 0
    return result


@router.post("/issue", status_code=201, responses={
                201: {"model": schema.Response, "description": "Post items success"}})
async def capture_issues(data: dict):
    result = await sentry_controller.capture_issues(data)
    return schema.Response(**result)
