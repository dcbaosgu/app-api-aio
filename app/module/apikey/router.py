from fastapi import APIRouter, Query
from . import schema
from .controller import APIKeyController


router = APIRouter(prefix="/v1/apikey", tags=["APIKEY"])
controller = APIKeyController()


@router.post("/generate", status_code=200, responses={
                200: {"model": schema.APIKeyRequest, "description": "Create items success"}})
async def generate_api_key(data: schema.APIKeyRequest):
    result = await controller.generate_api_key(data.model_dump())
    return schema.APIKeyResponse(**result)

@router.post("/encode", status_code=200, responses={
                200: {"description": "Create items success"}})
async def encode_api_key(token: str):
    result = await controller.encode_api_key(token)
    return schema.EncodeResponse(**result)

@router.post("/verify", status_code=200, responses={
                200: {"description": "Validate items success"}})
async def verify_key(apikey: str, hashkey: str):
    result = await controller.verify_key(apikey, hashkey)
    return result