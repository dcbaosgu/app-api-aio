from .service import tax_service

class TaxController:
    def __init__(self):
        self.service = tax_service

    async def get_tax(self, tax_code):
        result = await self.service.get_tax(tax_code)
        return result