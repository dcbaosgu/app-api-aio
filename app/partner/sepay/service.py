import requests
from .config import *
from .exception import ErrorCode
from fastapi.responses import StreamingResponse

class SepayService:
    def __init__(self):
        self.base_url = "https://qr.sepay.vn/img"

    def generate_qrpay(self, data):
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

sepay_service = SepayService()
