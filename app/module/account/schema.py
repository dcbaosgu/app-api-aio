from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    account: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetOTPRequest(BaseModel):
    email: EmailStr

class ResetOTPResponse(BaseModel):
    status: str
    message: str


class ForgotPasswordRequest(BaseModel):
    account: str
    reset_otp: str
    new_password: str

class ForgotPasswordResponse(BaseModel):
    status: str
    message: str
