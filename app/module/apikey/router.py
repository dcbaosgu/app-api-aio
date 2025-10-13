from fastapi import APIRouter, Query
from . import schema
from .controller import APIKeyController
from typing import Optional


router = APIRouter(prefix="/v1/apikey", tags=["ApiKey"])
controller = APIKeyController()


@router.post("/generate", status_code=201, responses={
                201: {"model": schema.APIKeyResponse, "description": "Create items success"}})
async def generate_apikey(subject: str, keyname: str, prefix: str = Query(..., enum=["sk-", "org-", "whsec-"])):

    result = await controller.generate_apikey(subject, keyname, prefix)
    return schema.APIKeyResponse(**result)


@router.post("/verify", status_code=201, responses={
                201: {"model": schema.APIKeyVerify, "description": "Verify items success"}})
async def verify_apikey(subject: str, apikey: str):
    result = await controller.verify_apikey(subject, apikey)
    return schema.APIKeyVerify(**result)


@router.delete("/delete/{apikey_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_apikey(apikey_id: str):
    result = await controller.delete(apikey_id)
    return result


@router.get("/search", status_code=200, responses={
                200: {"model": schema.PaginatedAPIKeyResponse, "description": "Get items success"}})
async def list_users(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search by subject name"),
):
    query = {}
    if search: query = {"subject": {"$regex": search, "$options": "i"}}
    
    result = await controller.search(query, page, limit)
    return result
