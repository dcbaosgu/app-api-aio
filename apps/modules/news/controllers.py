from .services import RSSService

class RSSController:
    def __init__(self):
        self.service = RSSService()

    async def list_rss(self, page: int, limit: int, category: str, search: str = None):
        result = await self.service.get_paginated(page, limit, category, search)
        return result
