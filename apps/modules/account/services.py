from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_aio
from apps.auth.services import auth_services
from worker.rabbitmq.services import RabbitMQServices
from .schemas import LoginRequest, ForgotPasswordRequest
from apps.utils.helper import Helper
from .exception import ErrorCode

account_crud = BaseCRUD("users", engine_aio)

class AccountService:
    def __init__(self, account_crud: BaseCRUD):
        self.account_crud = account_crud
        self.rabbitmq_service = RabbitMQServices()

    async def login(self, data: LoginRequest):
        email = data.email
        user = await self.account_crud.get_one_query({"email": email})
        if not user:
            raise ErrorCode.InvalidLogin()

        if not auth_services.check_password(data.password, user["password"].encode()):
            raise ErrorCode.InvalidLogin()

        token_data = {
            "uid": str(user.get("_id")),
            "email": user.get("email"),
            "permission": user.get("permission"),
            "remember_me": data.remember_me
        }
        token = await auth_services.encode_access_token(token_data)

        return {"token_type": "bearer", "access_token": token}

    async def get_otp(self, email: str):
        user = await self.account_crud.get_one_query({"email": email})
        if not user: 
            raise ErrorCode.EmailNotFound()

        otp_code = Helper.generate_secret_otp()
        expire_otp = Helper.get_timestamp() + 15 * 60

        await self.account_crud.update_by_id(_id=user["_id"], data={"otp_code": otp_code, "expire_otp": expire_otp})

        await self.rabbitmq_service.producer(
            email=user["email"],
            fullname=user["fullname"],
            data={"otp_code": otp_code},
            mail_type="reset_password"
        )
        return {"message": f"OTP sent to {email} & valid for 15 minutes"}
    
    async def clean_otp(self):
        now = Helper.get_timestamp()
        query = {"expire_otp": {"$lt": now}} # otp has expired
        data = {"$unset": {"expire_otp": "", "otp_code": ""}}
        
        result = await self.account_crud.update_many_nomit(query, data)
        return result
    
    async def forgot_password(self, data: ForgotPasswordRequest):
        user = await self.account_crud.get_one_query({"email": data.email})
        if not user:
            raise ErrorCode.EmailNotFound()
        
        if "otp_code" not in user or "expire_otp" not in user:
            raise ErrorCode.OTPNotFound()
        
        if user["otp_code"] != data.otp_code:
            raise ErrorCode.InvalidOTP()
        
        if Helper.get_timestamp() > user["expire_otp"]:
            raise ErrorCode.ExpiredOTP()
        
        hashed_password = (await auth_services.hash_password(data.new_password)).decode()

        await self.account_crud.update_one_nomit(
            {"_id": user["_id"]},
            {
                "$set": {"password": hashed_password},
                "$unset": {"otp_code": "", "expire_otp": ""}
            })
        return {"message": "Password has been reset successfully"}
