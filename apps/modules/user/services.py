from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_aio
from apps.utils.validator import Validator
from apps.auth.services import auth_services
from .exception import ErrorCode

user_crud = BaseCRUD("users", engine_aio)

class UserServices:
    def __init__(self, user_crud: BaseCRUD):
        self.user_crud = user_crud

    async def create(self, data: dict):

        if await Validator.is_field_exist(crud=self.user_crud, field="email", value=data.get("email")):
            raise ErrorCode.AccountExisted(data.get("email"))
        
        if await Validator.is_field_exist(crud=self.user_crud, field="phone", value=data.get("phone")):
            raise ErrorCode.AccountExisted(data.get("phone"))
        
        if data.get("password"):
            data["password"] = (await auth_services.hash_password(data["password"])).decode()

        return await self.user_crud.create(data)

    async def update(self, _id: str, data: dict):
        
        if await Validator.is_field_exist(crud=self.user_crud, field="email", value=data.get("email")):
            raise ErrorCode.AccountExisted(data.get("email"))
        
        if await Validator.is_field_exist(crud=self.user_crud, field="phone", value=data.get("phone")):
            raise ErrorCode.AccountExisted(data.get("phone"))
        
        if data.get("password"):
            data["password"] = (await auth_services.hash_password(data["password"])).decode()

        result = await self.user_crud.update_by_id(_id, data)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result
    
    async def get(self, _id):
        result = await self.user_crud.get_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result

    async def delete(self, _id):
        result = await self.user_crud.delete_by_id(_id)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.user_crud.search(query, page, limit)
        return result
