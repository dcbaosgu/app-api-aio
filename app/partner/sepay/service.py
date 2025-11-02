import requests
from .config import *
from .exception import ErrorCode
from fastapi.responses import StreamingResponse
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from app.utils.validator import Validator
from worker.telegram.service import sepay_bot


sepay_crud = BaseCRUD("sepay", engine_aio)

class SepayService:
    def __init__(self):
        self.base_url = "https://qr.sepay.vn/img"
        self.sepay_crud = sepay_crud

    def sepay_qrcode(self, data):
        param = f"acc={VIRTUAL_ACCOUNT}&bank={BANK_NAME}"

        if data.get("amount"):
            param += f"&amount={data['amount']}"
        if data.get("des"):
            param += f"&des={data['des']}"

        qr_url = f"{self.base_url}?{param}"

        try:
            result = requests.get(qr_url, stream=True)
        except Exception:
            raise ErrorCode.GenerateQRFailed()

        return StreamingResponse(
            result.raw, media_type=result.headers.get("content-type", "image/png"),
            headers={"Content-Disposition": 'inline; filename=\"qr.png\"'} # inline -> attachment (download)
        )
    
    def sepay_infopay(self, data):
        result = {
            "virtual_account": VIRTUAL_ACCOUNT,
            "bank_name": BANK_NAME,
            "amount": data.get("amount"),
            "description": data.get("des")
        }
        return result

    async def sepay_webhook(self, request, data):

        auth = request.headers.get("Authorization")

        if not Validator.is_apikey_valid(auth=auth, key=SEPAY_API_KEY):
            raise ErrorCode.SepayUnauthorized()
        
        try:
            transaction = {
                "sepay_id": data["id"],
                "gateway": data["gateway"],
                "transaction_date": Helper.date_to_timestamp(
                    dt=data["transactionDate"], fmt="%Y-%m-%d %H:%M:%S"
                ),
                "account_number": data["accountNumber"],
                "code": data.get("code"),
                "content": data.get("content"),
                "transfer_type": data["transferType"],
                "transfer_amount": float(data["transferAmount"]),
                "accumulated": float(data["accumulated"]) if data.get("accumulated") else None,
                "sub_account": data.get("subAccount"),
                "reference_code": data.get("referenceCode"),
                "description": data.get("description"),
            }

            await sepay_bot.send_telegram(transaction)
            result = await self.sepay_crud.create(transaction)

            return {"status": "success", "_id": str(result.inserted_id)}

        except Exception as e:
            print(f"[Sepay Webhook Error] {e}")
            raise ErrorCode.SepayWebhookFailed()

sepay_service = SepayService()
