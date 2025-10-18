from .service import apikey_service

class APIKeyController:
    def __init__(self):
        self.service = apikey_service

    async def generate_api_key(self, data):
        result = await self.service.generate_api_key(data)
        return result

    async def encode_api_key(self, token):
        result = await self.service.encode_api_key(token)
        return result