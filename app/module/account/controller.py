from .service import account_service


class AccountController:
    def __init__(self):
        self.service = account_service

    async def login(self, data):
        result = await self.service.login(data)
        return result
    
    async def reset_otp(self, data):
        result = await self.service.reset_otp(data)
        return result
    
    async def clean_otp(self):
        result = await self.service.clean_otp()
        return result

    async def forgot_password(self, data):
        result = await self.service.forgot_password(data)
        return result