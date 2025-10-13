from .service import home_service


class HomeController:
    def __init__(self):
        self.service = home_service

    async def backup_db(self):
        result = await self.service.backup_db()
        return result
    
    async def search(self, query: dict, page: int, limit: int, start_time: str, end_time: str):
        result = await self.service.search(query, page, limit, start_time, end_time)
        return result