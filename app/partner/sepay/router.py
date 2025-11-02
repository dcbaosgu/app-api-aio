from fastapi import APIRouter, Request, Query
from . import schema
from .controller import SepayController

router = APIRouter(prefix="/v1/sepay", tags=["Sepay"])
controller = SepayController()


@router.post("/payment", status_code=200, responses={
                200: {"model": schema.GenerateQRPay, "description": "Create items success"}})
def sepay_payment(data: schema.GenerateQRPay, category: str = Query(..., enum=["qr-code", "info-pay"])):
    result = controller.sepay_payment(data.model_dump(), category)
    return result

@router.post("/webhook", status_code=200, responses={
                200: {"model": schema.SepayWebhook, "description": "Create items success"}})
async def sepay_webhook(request: Request, data: schema.SepayWebhook):
    result = await controller.sepay_webhook(request, data.model_dump())
    return result
