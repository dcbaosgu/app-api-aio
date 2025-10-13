from .service import cron_service


class CronController:
    def __init__(self):
        self.service = cron_service

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def getdb(self, cron_id):
        result = await self.service.getdb(cron_id)
        return result
    
    async def runtime(self):
        result = await self.service.runtime()
        return result
    
    async def update(self, cron_id, data):
        result = await self.service.update(cron_id, data)
        return result

    async def delete(self, cron_id):
        result = await self.service.delete(cron_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
