from jose import jwt
from io import BytesIO
from bson import ObjectId
from typing import Literal
from fastapi import Response
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from app.auth.config import SECRET_KEY, ALGORITHM
from app.utils.validator import Validator
import random, secrets, uuid, hmac, hashlib
import string, base64, qrcode, unicodedata, re

class Helper:
    
    @staticmethod
    def _key(user_id: str) -> str:
        result = f"cart:{user_id}"
        return result
    
    @staticmethod
    def _recalc(cart: dict) -> dict:
        total_items = sum(it.quantity for it in cart.items)
        total_price = sum(it.price * it.quantity for it in cart.items)
        cart.total_items = total_items
        cart.total_price = total_price
        cart.last_update = Helper.get_timestamp()
        return cart
    
    @staticmethod
    def get_timestamp(tz: str = "UTC") -> float:
        now = datetime.now(ZoneInfo(tz))
        return now.timestamp()

    @staticmethod
    def object_to_string(doc: dict) -> dict:
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    @staticmethod
    def string_to_object(query: dict) -> dict:
        if "_id" in query and isinstance(query["_id"], str) and Validator.is_object_id(query["_id"]):
            query["_id"] = ObjectId(query["_id"])
        return query
    
    @staticmethod
    def get_future_timestamp(days_to_add: int, timezone: str = "UTC") -> float:
        current_date = datetime.now(ZoneInfo(timezone))
        future_date = current_date + timedelta(days=days_to_add)
        return future_date.timestamp() 
    
    @staticmethod
    def convert_slug(text: str) -> str:
        """Convert a string with accents and special characters into a URL-friendly slug"""
        # Normalize unicode to remove accents (e.g., é -> e, ư -> u)
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = text.lower()

        # Replace non-alphanumeric characters with hyphens
        text = re.sub(r"[^a-z0-9]+", "-", text)
        # Remove leading/trailing hyphens
        text = text.strip("-")
        
        return text

    @staticmethod
    def timestamp_to_date(ts: float, fmt: str = "%d-%m-%Y %H:%M:%S", tz: str = "UTC") -> str:
        # Convert timestamp (e.g., 1755688756) to date string "20-08-2025 22:59:16"
        # Timezone ex: Asia/Tokyo, None, UTC,...
        result = datetime.fromtimestamp(float(ts), tz=ZoneInfo(tz))
        return result.strftime(fmt)

    @staticmethod
    def date_to_timestamp(dt: str, fmt: str = "%d-%m-%Y %H:%M:%S", tz: str = "UTC") -> float:
        # Convert date string "20-08-2025 22:59:16" to timestamp (e.g., 1755688756.0)
        result = datetime.strptime(dt, fmt)
        result = result.replace(tzinfo=ZoneInfo(tz))
        return result.timestamp()
    
    @staticmethod
    def generate_ticket_code() -> str:
        # Generate ticket code of first 5 letters + 12 random numbers, for example LYPJR714855620195
        prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
        number = ''.join(random.choices(string.digits, k=2))
        timestamp = str(int(Helper.get_timestamp()))
        return f"{prefix}{number}{timestamp}"
    
    @staticmethod
    async def decode_access_token(token: str) -> dict:
        result = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return result
    
    @staticmethod
    def generate_secret_otp(length: int = 6) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            result = ''.join(secrets.choice(chars) for _ in range(length))
            if sum(c.isalpha() for c in result) >= 2 and sum(c.isdigit() for c in result) >= 2:
                return result
            
    @staticmethod
    def generate_qr_code(data: str, format: Literal["base64", "image"]):
        qr = qrcode.make(data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        if format == "base64":
            b64 = base64.b64encode(image_bytes).decode("utf-8")
            result = {"data": data,"qr_code": f"data:image/png;base64,{b64}"}
        else:
            result = Response(content=image_bytes, media_type="image/png")
            # headers={"Content-Disposition": f"attachment; filename=qr_{data}.png"} # Download
        return result
        
    def generate_key_v1(prefix: str = "sk", length: int = 64) -> str:
        token = ''
        while len(token) < length:
            token += secrets.token_urlsafe(length)
        return f"{prefix}-{token[:length]}"

    def generate_key_v2(prefix: str = "sk", length: int = 64) -> str:
        alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        return f"{prefix}-{token}"

    def generate_key_v3(prefix: str = "sk", length: int = 64) -> str:
        token = ''
        while len(token) < length:
            key_bytes = uuid.uuid4().bytes
            token += base64.urlsafe_b64encode(key_bytes).decode().rstrip("=")
        return f"{prefix}-{token[:length]}"
    
    def encode_hmac_key(token):
        signature = hmac.new(
            key=SECRET_KEY.encode(),
            msg=token.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signature