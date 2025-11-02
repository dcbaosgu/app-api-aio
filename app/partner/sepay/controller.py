from .service import sepay_service

class SepayController:
    def __init__(self):
        self.service = sepay_service

    def sepay_payment(self, data, category):
        if category == "qr-code":
            result = self.service.sepay_qrcode(data)
        if category == "info-pay":
            result = self.service.sepay_infopay(data)
        return result
    
    async def sepay_webhook(self, request, data):
        result = await self.service.sepay_webhook(request, data)
        return result