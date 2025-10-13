from .service import user_service


class UserController:
    def __init__(self):
        self.service = user_service

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def get(self, user_id):
        result = await self.service.get(user_id)
        return result
    
    async def update(self, user_id, data):
        result = await self.service.update(user_id, data)
        return result

    async def delete(self, user_id):
        result = await self.service.delete(user_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
