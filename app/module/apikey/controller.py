from .service import apikey_service

class APIKeyController:
    def __init__(self):
        self.service = apikey_service

    async def generate_apikey(self, subject: str, keyname: str, prefix: str):
        result = await self.service.generate_apikey(subject, keyname, prefix)
        return result

    async def verify_apikey(self, subject: str, apikey: str):
        result = await self.service.verify_apikey(subject, apikey)
        return result

    async def delete(self, apikey_id):
        result = await self.service.delete(apikey_id)
        return result
    
    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result