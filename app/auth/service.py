from jose import jwt
from .config import *
from app.utils.helper import Helper
from bcrypt import checkpw, gensalt, hashpw


class AuthService():

    async def hash_password(self, password):
        result = hashpw(password.encode("utf8"), gensalt())
        return result

    def check_password(self, login_password, password):
        if not checkpw(login_password.encode("utf-8"), password):
            return False
        return True

    async def encode_access_token(self, data):
        data = data.copy()
        expire_days = (REMEMBER_TOKEN_DAY if data.get("remember_me") else ACCESS_TOKEN_EXPIRE_DAY)
        
        expire = Helper.get_future_timestamp(days_to_add=expire_days)
        
        data.update({"exp": expire})
        
        encode = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encode

auth_service = AuthService()