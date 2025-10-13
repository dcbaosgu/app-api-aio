from app.utils.helper import Helper
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from .exception import ErrorCode

product_crud = BaseCRUD("product", engine_aio)

class ProductServices:
    def __init__(self, product_crud: BaseCRUD):
        self.product_crud = product_crud
    
    async def create(self, data: dict):
        data["sku"] = Helper.convert_slug(data["name"])
        result = await self.product_crud.create(data)
        return result

    async def update(self, product_id, data):
        result = await self.product_crud.update_by_id(product_id, data)
        if not result:
            raise ErrorCode.InvalidProductId()
        return result

    async def get(self, product_id):
        result = await self.product_crud.get_by_id(product_id)
        if not result:
            raise ErrorCode.InvalidProductId()
        return result

    async def delete(self, product_id):
        result = await self.product_crud.delete_by_id(product_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.product_crud.search(query, page, limit)
        return result

    """
    async def add_serial(self, product_id: str, number: str, status: str):
        product = await self.product_crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        for s in product.get("serial", []):
            if s["number"] == number:
                raise ErrorCode.SerialAlreadyExists()

        payload = {"$push": {"serial": {"number": number, "status": status}}}
        await self.product_crud.update_one_nomit({"_id": product_id}, payload)
        return {"status": "success", "message": f"Serial {number} added successfully"}


    async def update_serial(self, product_id: str, number_old: str, number_new: str, status_new: str):
        product = await self.product_crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        found = False
        for s in product.get("serial", []):
            if s["number"] == number_old:
                found = True
                break
        if not found:
            raise ErrorCode.SerialNotFound()

        payload = {
            "$set": {
                "serial.$[elem].number": number_new,
                "serial.$[elem].status": status_new
            }
        }
        array_filters = [{"elem.number": number_old}]
        await self.product_crud.update_one_nomit({"_id": product_id}, payload, array_filters=array_filters)
        return {"status": "success", "message": f"Serial {number_old} updated to {number_new}"}


    async def delete_serial(self, product_id: str, number: str):
        product = await self.product_crud.get_by_id(product_id)
        if not product:
            raise ErrorCode.InvalidProductId()
        
        found = False
        for s in product.get("serial", []):
            if s["number"] == number:
                found = True
                break
        if not found:
            raise ErrorCode.SerialNotFound()

        payload = {"$pull": {"serial": {"number": number}}}
        await self.product_crud.update_one_nomit({"_id": product_id}, payload)
        return {"status": "success", "message": f"Serial {number} deleted successfully"}
    """
    
product_service = ProductServices(product_crud)