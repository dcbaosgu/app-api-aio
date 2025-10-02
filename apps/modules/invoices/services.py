from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_aio
from apps.utils.helper import Helper
from apps.utils.validator import Validator
from .exception import ErrorCode
from .schemas import InvoiceEmail, ItemEmail
from apps.modules.redis.services import CartService
from worker.rabbitmq.services import RabbitMQServices
from worker.telegram.services import invoice_bot
from apps.modules.user.services import user_crud
from apps.modules.product.services import product_crud

invoice_crud = BaseCRUD("invoices", engine_aio)

class InvoiceServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud
        self.cart_service = CartService()
        self.rabbitmq_service = RabbitMQServices()

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

        result = await self.crud.create(invoice_data)

        # Send mail to RabbitMQ
        user = await user_crud.get_by_id(cart["user_id"])
        email_data = InvoiceEmail(
            items=[ItemEmail(**item) for item in cart["items"]],
            address=cart.get("address"),
            note=cart.get("note"),
            total_items=cart.get("total_items"),
            total_price=cart.get("total_price")
        )
        await self.rabbitmq_service.producer(email=user.get("email"), fullname=user.get("fullname"), data=email_data.model_dump(), mail_type="bill_info")

        await self.cart_service.redis.delete(Helper._key(user_id))
        await invoice_bot.send_telegram(invoice_data)    

        return result

    async def update(self, _id, data: dict):
        result = await self.crud.update_by_id(_id, data)
        return result

    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
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

        result = await self.crud.search(query, page, limit)
        return result
