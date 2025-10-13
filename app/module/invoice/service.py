from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from app.utils.validator import Validator
from .exception import ErrorCode
from .schema import InvoiceEmail, ItemEmail
from app.module.redis.service import cart_service
from worker.rabbitmq.service import rabbitmq_service
from worker.telegram.service import invoice_bot
from app.module.user.service import user_crud
from app.module.product.service import product_crud

invoice_crud = BaseCRUD("invoice", engine_aio)

class InvoiceService:
    def __init__(self, invoice_crud: BaseCRUD):
        self.invoice_crud = invoice_crud
        self.cart_service = cart_service
        self.rabbitmq_service = rabbitmq_service

    async def checkout_cart(self, user_id: str):
        cart = await self.cart_service.get_cart(user_id)
        if not cart:
            raise ErrorCode.CartNotFound()
        if not cart.get("items"):
            raise ErrorCode.CartEmpty()
        
        for item in cart["items"]:
            product = await product_crud.get_by_id(item["product_id"])
            if not product:
                raise ErrorCode.ProductNotFound()
            
            if product.get("quantity", 0) <= 0 or item["quantity"] > product.get("quantity", 0):
                raise ErrorCode.InsufficientStock(product.get("name"), product.get("quantity"))
            
            # Update quantity after checkout cart
            await product_crud.update_by_id(item["product_id"], 
                {"quantity": product.get("quantity", 0) - item["quantity"]})

        invoice_data = {
            "user_id": cart["user_id"],
            "items": cart["items"],
            "address": cart.get("address"),
            "note": cart.get("note"),
            "total_items": cart.get("total_items", 0),
            "total_price": cart.get("total_price", 0.0),
            "type_vat": cart.get("type_vat"),
            "status": "pending",
            "created_at": Helper.get_timestamp()}

        result = await self.invoice_crud.create(invoice_data)

        # Send mail to RabbitMQ
        user = await user_crud.get_by_id(cart["user_id"])
        
        email_data = InvoiceEmail(
            items=[ItemEmail(**item) for item in cart["items"]],
            address=cart.get("address"),
            note=cart.get("note"),
            total_items=cart.get("total_items"),
            total_price=cart.get("total_price")
        )
        await self.rabbitmq_service.producer(
            email=user.get("email"), fullname=user.get("fullname"), 
            data=email_data.model_dump(), mail_type="issue_invoice")

        await self.cart_service.redis.delete(Helper._key(user_id))
        await invoice_bot.send_telegram(invoice_data)    

        return result

    async def update(self, invoice_id, data: dict):
        result = await self.invoice_crud.update_by_id(invoice_id, data)
        return result

    async def get(self, invoice_id):
        result = await self.invoice_crud.get_by_id(invoice_id)
        return result

    async def delete(self, invoice_id):
        result = await self.invoice_crud.delete_by_id(invoice_id)
        return result

    async def search(self, query: dict, page: int, limit: int, start_time: str, end_time: str):

        if start_time:
            if not Validator.is_valid_date(start_time):
                raise ErrorCode.InvalidDateFormat()
            
            start_timestamp = Helper.date_to_timestamp(dt=start_time, tz="Asia/Ho_Chi_Minh")
            query.setdefault("created_at", {})
            query["created_at"]["$gte"] = start_timestamp

        if end_time:
            if not Validator.is_valid_date(end_time):
                raise ErrorCode.InvalidDateFormat()
            
            end_timestamp = Helper.date_to_timestamp(dt=end_time, tz="Asia/Ho_Chi_Minh")
            query.setdefault("created_at", {})
            query["created_at"]["$lte"] = end_timestamp

        result = await self.invoice_crud.search(query, page, limit)
        return result


invoice_service = InvoiceService(invoice_crud)