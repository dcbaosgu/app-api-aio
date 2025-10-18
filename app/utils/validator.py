import re, secrets
from bson import ObjectId
from datetime import datetime

class Validator:

    @staticmethod
    def is_object_id(_id: str) -> bool:
        result =  ObjectId.is_valid(_id)
        return result
    
    @staticmethod
    async def is_field_exist(crud, field: str, value: str, exclude_id: str = None) -> bool:
        if not value:
            return False
        query = {field: value}
        if exclude_id: # Ignore records with ID
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        result = await crud.get_one_query(query=query) is not None
        return result
    
    @staticmethod
    def is_password_valid(password: str) -> bool:
        if not 8 <= len(password) <= 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
    
    @staticmethod
    def is_valid_date(date_str: str, fmt: str = "%d-%m-%Y %H:%M:%S") -> bool:
        if not date_str: return False
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_apikey_valid(auth, key) -> bool:
        if not auth: 
            return False
        # Ex: "Apikey 123abc" or "Bearer 123abc"
        token = auth.split(" ", 1)[1].strip()
        if not secrets.compare_digest(token, key):
            return False
        return True