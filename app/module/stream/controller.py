from .service import steam_service


class StreamController:
    def __init__(self):
        self.service = steam_service

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def get(self, stream_id):
        result = await self.service.get(stream_id)
        return result
    
    async def update(self, stream_id, data):
        result = await self.service.update(stream_id, data)
        return result

    async def delete(self, stream_id):
        result = await self.service.delete(stream_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result

    async def play_list(self, stream_id: str):
        result = await self.service.play_list(stream_id)
        return result
    
    async def play_master(self, stream_id: str, resolution: str):
        result = await self.service.play_master(stream_id, resolution)
        return result
