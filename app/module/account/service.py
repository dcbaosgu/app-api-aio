from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.auth.service import auth_service
from worker.rabbitmq.service import rabbitmq_service
from .schema import LoginRequest, ForgotPasswordRequest
from app.utils.helper import Helper
from .exception import ErrorCode


account_crud = BaseCRUD("user", engine_aio)

class AccountService:
    def __init__(self, account_crud: BaseCRUD):
        self.account_crud = account_crud
        self.auth_service = auth_service
        self.rabbitmq_service = rabbitmq_service

    async def login(self, data: LoginRequest):
        user = await self.account_crud.get_one_query({
            "$or": [{"email": data.account}, {"phone": data.account}]
        })

        if not user: raise ErrorCode.InvalidLogin()

        if not self.auth_service.check_password(data.password, user["password"].encode()):
            raise ErrorCode.InvalidLogin()

        token_data = {
            "uid": str(user.get("_id")),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "permission": user.get("permission"),
            "remember_me": data.remember_me
        }
        token = await self.auth_service.encode_access_token(token_data)

        return {"token_type": "bearer", "access_token": token}

    async def get_otp(self, email: str):
        user = await self.account_crud.get_one_query({"email": email})

        if not user: raise ErrorCode.UserNotFound()

        otp_code = Helper.generate_secret_otp()
        expire_otp = Helper.get_timestamp() + 15 * 60

        await self.account_crud.update_by_id(_id=user["_id"], data={"otp_code": otp_code, "expire_otp": expire_otp})

        await self.rabbitmq_service.producer(
            email=user.get("email"), fullname=user.get("fullname"),
            data={"otp_code": otp_code}, mail_type="reset_password")

        result = {"status":"success", "message": f"OTP sent: {email} & valid for 15 min"}
        return result
    
    async def clean_otp(self):
        now = Helper.get_timestamp()
        query = {"expire_otp": {"$lt": now}} # otp has expired
        data = {"$unset": {"expire_otp": "", "otp_code": ""}}
        
        result = await self.account_crud.update_many_nomit(query, data)
        return result
    
    async def forgot_password(self, data: ForgotPasswordRequest):
        user = await self.account_crud.get_one_query({
            "$or": [{"email": data.account}, {"phone": data.account}]
        })
        if not user: raise ErrorCode.UserNotFound()
        
        if "otp_code" not in user or "expire_otp" not in user:
            raise ErrorCode.OTPNotFound()
        
        if user["otp_code"] != data.otp_code:
            raise ErrorCode.InvalidOTP()
        
        if Helper.get_timestamp() > user["expire_otp"]:
            raise ErrorCode.ExpiredOTP()
        
        hashed_password = (await self.auth_service.hash_password(data.new_password)).decode()

        await self.account_crud.update_one_nomit(
            {"_id": user["_id"]},
            {
                "$set": {"password": hashed_password},
                "$unset": {"otp_code": "", "expire_otp": ""}
            })
        result = {"status": "success", "message": "Password has been reset"}
        return result
    

account_service = AccountService(account_crud)
