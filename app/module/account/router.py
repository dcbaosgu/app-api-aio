from fastapi import APIRouter
from . import schema 
from .controller import AccountController
from app.auth.depend import require_permission


router = APIRouter(prefix="/v1/account", tags=["Account"])
controller = AccountController()


@router.get("/get-me", status_code=200, 
            responses={200: {"description": "Get items success"}})
async def get_me(current_user: dict = require_permission()):
    result = {"user": current_user}
    return result

@router.post("/login", status_code=201, responses={
                201: {"model": schema.LoginResponse, "description": "Post items success"}})
async def login(data: schema.LoginRequest):
    result = await controller.login(data)
    return result

@router.post("/reset-otp", status_code=201, responses={
                201: {"model": schema.ResetOTPResponse, "description": "Post items success"}})
async def reset_otp(data: schema.ResetOTPRequest):
    result = await controller.reset_otp(data)
    return result

@router.post("/clean-otp", status_code=201, responses={
                201: {"description": "Clean items success"}})
async def clean_otp():
    result = await controller.clean_otp()
    return result

@router.post("/forgot-password", status_code=201, responses={
                201: {"model": schema.ForgotPasswordRequest, "description": "Post items success"}})
async def forgot_password(data: schema.ForgotPasswordRequest):
    result = await controller.forgot_password(data)
    return result