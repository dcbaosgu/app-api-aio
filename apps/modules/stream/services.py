from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_aio
from .exception import ErrorCode

stream_crud = BaseCRUD("stream-videos", engine_aio)

class StreamServices:
    def __init__(self, stream_crud: BaseCRUD):
        self.stream_crud = stream_crud

    async def create(self, data: dict):
        result = await self.stream_crud.create(data)      
        return result

    async def update(self, _id: str, data: dict):
        result = await self.stream_crud.update_by_id(_id, data)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result
    
    async def get(self, _id):
        result = await self.stream_crud.get_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result

    async def delete(self, _id):
        result = await self.stream_crud.delete_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidStreamId()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.stream_crud.search(query, page, limit)
        return result
