from .services import cron_crud, CronServices


class CronController:
    def __init__(self):
        self.service = CronServices(cron_crud)

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def getdb(self, _id):
        result = await self.service.getdb(_id)
        return result
    
    async def runtime(self):
        result = await self.service.runtime()
        return result
    
    async def update(self, _id, data):
        result = await self.service.update(_id, data)
        return result

    async def delete(self, _id):
        result = await self.service.delete(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
