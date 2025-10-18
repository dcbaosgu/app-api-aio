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

class SepayWebhook(BaseModel):
    id: int
    gateway: str
    transactionDate: str
    accountNumber: str
    code: Optional[str] = None
    content: Optional[str] = None
    transferType: str
    transferAmount: Decimal
    accumulated: Optional[Decimal] = None
    subAccount: Optional[str] = None
    referenceCode: Optional[str] = None
    description: Optional[str] = None

    @validator('transferAmount', 'accumulated', pre=True)
    def convert_decimal(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v