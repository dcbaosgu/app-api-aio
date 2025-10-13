from .service import account_service
from .schema import LoginRequest, GetOTPRequest, ForgotPasswordRequest


class AccountController:
    def __init__(self):
        self.service = account_service

    async def login(self, data: LoginRequest):
        result = await self.service.login(data)
        return result
    
    async def get_otp(self, data: GetOTPRequest):
        result = await self.service.get_otp(data.email)
        return result
    
    async def clean_otp(self):
        result = await self.service.clean_otp()
        return result

    async def forgot_password(self, data: ForgotPasswordRequest):
        result = await self.service.forgot_password(data)
        return result