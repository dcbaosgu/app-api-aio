from app.auth.service import auth_service
from app.module.user.service import user_crud
from worker.rabbitmq.service import rabbitmq_service
from .schema import LoginRequest, ForgotPasswordRequest
from app.utils.helper import Helper
from .exception import ErrorCode

class AccountService:
    def __init__(self):
        self.user_crud = user_crud
        self.auth_service = auth_service
        self.rabbitmq_service = rabbitmq_service

    async def login(self, data: LoginRequest):
        user = await self.user_crud.get_one_query({
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

    async def reset_otp(self, data: str):
        user = await self.user_crud.get_one_query({"email": data.email})

        if not user: raise ErrorCode.UserNotFound()

        reset_otp = Helper.generate_secret_otp()
        reset_exp = Helper.get_timestamp() + 15 * 60

        await self.user_crud.update_by_id(_id=user["_id"], data={"reset_otp": reset_otp, "reset_exp": reset_exp})

        await self.rabbitmq_service.producer(
            email=user.get("email"), fullname=user.get("fullname"),
            data=reset_otp, mail_type="reset_password")

        result = {"status":"success", "message": f"OTP sent: {data.email} & valid for 15 min"}
        return result
    
    async def clean_otp(self):
        now = Helper.get_timestamp()
        query = {"reset_exp": {"$lt": now}} # OTP has expired
        data = {"$unset": {"reset_exp": "", "reset_otp": ""}}
        
        result = await self.user_crud.update_many_nomit(query, data)
        return result
    
    async def forgot_password(self, data: ForgotPasswordRequest):
        user = await self.user_crud.get_one_query({
            "$or": [{"email": data.account}, {"phone": data.account}]
        })
        if not user: raise ErrorCode.UserNotFound()
        
        if "reset_otp" not in user or "reset_exp" not in user:
            raise ErrorCode.OTPNotFound()
        
        if user["reset_otp"] != data.reset_otp:
            raise ErrorCode.InvalidOTP()
        
        if Helper.get_timestamp() > user["reset_exp"]:
            raise ErrorCode.ExpiredOTP()
        
        hashed_password = (await self.auth_service.hash_password(data.new_password)).decode()

        await self.user_crud.update_one_nomit(
            {"_id": user["_id"]},
            {
                "$set": {"password": hashed_password},
                "$unset": {"reset_otp": "", "reset_exp": ""}
            })
        result = {"status": "success", "message": "Password has been reset"}
        return result
    

account_service = AccountService()
