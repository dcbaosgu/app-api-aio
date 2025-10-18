from .service import sepay_service

class SepayController:
    def __init__(self):
        self.service = sepay_service

    def generate_qrpay(self, data):
        result = self.service.generate_qrpay(data)
        return result
    
    async def sepay_webhook(self, request, data):
        result = await self.service.sepay_webhook(request, data)
        return result