from .service import invoice_service


class InvoiceController:
    def __init__(self):
        self.service = invoice_service

    async def checkout_cart(self, user_id: str):
        result = await self.service.checkout_cart(user_id)
        return result

    async def get(self, invoice_id: str):
        result = await self.service.get(invoice_id)
        return result

    async def update(self, invoice_id: str, data: dict):
        result = await self.service.update(invoice_id, data)
        return result

    async def delete(self, invoice_id: str):
        result = await self.service.delete(invoice_id)
        return result

    async def search(self, query: dict, page: int, limit: int, start_time: str, end_time: str):
        result = await self.service.search(query, page, limit, start_time, end_time)
        return result
