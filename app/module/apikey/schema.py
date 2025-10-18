from pydantic import BaseModel
from typing import List

class APIKeyRequest(BaseModel):
    prefix: str = "sk"
    length: int = 64

class APIKeyResponse(BaseModel):
    key_v1: str
    key_v2: str
    key_v3: str

class EncodeResponse(BaseModel):
    status : str
    encode_key: str