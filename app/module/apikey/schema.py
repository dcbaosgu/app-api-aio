from pydantic import BaseModel
from typing import List

class APIKeyResponse(BaseModel):
    subject: str
    keyname: str
    apikey: str

class APIKeyVerify(BaseModel):
    status: str
    verify: bool

class PaginatedAPIKeyResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    results: List[APIKeyResponse]
