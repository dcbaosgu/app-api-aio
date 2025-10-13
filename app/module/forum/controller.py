from .service import thread_service, post_service


class ThreadController:
    def __init__(self):
        self.service = thread_service

    async def create(self, data): 
        result = await self.service.create(data)
        return result
    
    async def get(self, thread_id): 
        result = await self.service.get(thread_id)
        return result
    
    async def update(self, thread_id, data): 
        result = await self.service.update(thread_id, data)
        return result
    
    async def delete(self, thread_id): 
        result = await self.service.delete(thread_id)
        return result
    
    async def search(self, query, page, limit): 
        result = await self.service.search(query, page, limit)
        return result


class PostController:
    def __init__(self):
        self.service = post_service

    async def create(self, data):   
        result = await self.service.create(data)
        return result
    
    async def get(self, post_id): 
        result = await self.service.get(post_id)
        return result
    
    async def update(self, post_id, data): 
        result = await self.service.update(post_id, data)
        return result

    async def delete(self, post_id):
        result = await self.service.delete(post_id)
        return result

    async def search(self, query, page, limit): 
        result = await self.service.search(query, page, limit)
        return result

    async def reaction(self, post_id: str, reaction: str, user_id: str):
        result = await self.service.reaction(post_id, reaction, user_id)
        return result