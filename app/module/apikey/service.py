from app.utils.helper import Helper


class APIKeyService:
    def __init__(self):
        pass

    async def generate_api_key(self, data):
        key_v1 = Helper.generate_key_v1(prefix=data["prefix"], length=data["length"])
        key_v2 = Helper.generate_key_v2(prefix=data["prefix"], length=data["length"])
        key_v3 = Helper.generate_key_v3(prefix=data["prefix"], length=data["length"])
        result = {"key_v1": key_v1, "key_v2": key_v2, "key_v3": key_v3}
        return result

    async def encode_api_key(self, token):
        encode_key = Helper.encode_hmac_key(token)
        result = {"status": "success", "encode_key": encode_key}
        return result

apikey_service = APIKeyService()