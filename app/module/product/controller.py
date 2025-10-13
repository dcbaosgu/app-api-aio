from .service import product_service

class ProductController:
    def __init__(self):
        self.service = product_service

    async def create(self, data):
        result = await self.service.create(data)
        return result
    
    async def get(self, product_id):
        result = await self.service.get(product_id)
        return result
    
    async def update(self, product_id, data):
        result = await self.service.update(product_id, data)
        return result

    async def delete(self, product_id):
        result = await self.service.delete(product_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
    
    """
    async def add_serial(self, product_id, number, status):
        result = await self.service.add_serial(product_id, number, status)
        return result

    async def update_serial(self, product_id, number_old, number_new, status_new):
        result = await self.service.update_serial(product_id, number_old, number_new, status_new)
        return result

    async def delete_serial(self, product_id, number):
        result = await self.service.delete_serial(product_id, number)
        return result
    """