import uuid, hmac, hashlib
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from .exception import ErrorCode
from .config import  SECRET_KEY

apikey_crud = BaseCRUD("api-key", engine_aio)


class APIKeyService:
    def __init__(self, apikey_crud: BaseCRUD):
        self.apikey_crud = apikey_crud
        

    async def generate_apikey(self, subject: str, keyname: str, prefix: str):
        query = {"subject": subject, "keyname": keyname}
        exist = await self.apikey_crud.get_one_query(query)

        if exist: raise ErrorCode.SubjectExisted(subject)

        apikey = f"{prefix}{uuid.uuid4().hex}"

        hashkey = hmac.new(
            SECRET_KEY.encode(), 
            apikey.encode(), 
            hashlib.sha256).hexdigest()

        data = {"subject": subject, "keyname": keyname, "hash_key": hashkey}
        await self.apikey_crud.create(data)

        result = {"subject": subject, "keyname": keyname, "apikey": apikey}
        return result
    

    async def verify_apikey(self, subject: str, apikey: str) -> bool:
        hashkey = hmac.new(
            SECRET_KEY.encode(),
            apikey.encode(),
            hashlib.sha256).hexdigest()
        
        query = {"subject": subject, "hash_key": hashkey}
        verify = await self.apikey_crud.get_one_query(query)
        
        result = {"status": "success", "verify": bool(verify)}
        return result
    

    async def delete(self, apikey_id):
        result = await self.apikey_crud.delete_by_id(apikey_id)
        if not result: 
            raise ErrorCode.InvalidAPIKeyId()
        return result


    async def search(self, query: dict, page: int, limit: int):
        result = await self.apikey_crud.search(query, page, limit)
        return result


apikey_service = APIKeyService(apikey_crud)