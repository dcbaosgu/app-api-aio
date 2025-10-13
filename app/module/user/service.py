from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.validator import Validator
from app.auth.service import auth_service
from .exception import ErrorCode

user_crud = BaseCRUD("user", engine_aio)

class UserService:
    def __init__(self, user_crud: BaseCRUD):
        self.user_crud = user_crud
        self.auth_service = auth_service

    async def create(self, data: dict):

        if await Validator.is_field_exist(crud=self.user_crud, field="email", value=data.get("email")):
            raise ErrorCode.AccountExisted(data.get("email"))
        
        if await Validator.is_field_exist(crud=self.user_crud, field="phone", value=data.get("phone")):
            raise ErrorCode.AccountExisted(data.get("phone"))
        
        if data.get("password"):
            data["password"] = (await self.auth_service.hash_password(data["password"])).decode()

        return await self.user_crud.create(data)

    async def update(self, user_id: str, data: dict):
        
        if await Validator.is_field_exist(crud=self.user_crud, field="email", value=data.get("email")):
            raise ErrorCode.AccountExisted(data.get("email"))
        
        if await Validator.is_field_exist(crud=self.user_crud, field="phone", value=data.get("phone")):
            raise ErrorCode.AccountExisted(data.get("phone"))
        
        if data.get("password"):
            data["password"] = (await self.auth_service.hash_password(data["password"])).decode()

        result = await self.user_crud.update_by_id(user_id, data)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result
    
    async def get(self, user_id):
        result = await self.user_crud.get_by_id(user_id)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result

    async def delete(self, user_id):
        result = await self.user_crud.delete_by_id(user_id)
        if not result: 
            raise ErrorCode.InvalidUserId()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.user_crud.search(query, page, limit)
        return result


user_service = UserService(user_crud)