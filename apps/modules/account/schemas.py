from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    account: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GetOTPRequest(BaseModel):
    email: EmailStr

class GetOTPResponse(BaseModel):
    status: str
    message: str


class ForgotPasswordRequest(BaseModel):
    account: str
    otp_code: str
    new_password: str

class ForgotPasswordResponse(BaseModel):
    status: str
    message: str
