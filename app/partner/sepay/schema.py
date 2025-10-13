from decimal import Decimal
from bson.decimal128 import Decimal128
from pydantic import BaseModel, validator
from typing import Optional

class GenerateQRPay(BaseModel):
    amount: Optional[Decimal] = None
    des: str

    @validator('amount')
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v
    