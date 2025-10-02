import io, zipfile, bson
from fastapi import Response
from .exception import ErrorCode
from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_logs, engine_aio
from apps.utils.helper import Helper
from apps.utils.validator import Validator


logging_crud = BaseCRUD("loggings", engine_logs)

class HomeService:

    async def export_bson(self) -> dict[str, list[dict]]:
        # Get all data from all collections in AIO
        collections_data = {}
        collections = await engine_aio.list_collection_names()
        for collection_name in collections:
            collection = engine_aio.get_collection(collection_name)
            documents = []
            async with collection.find({}) as cursor:
                async for doc in cursor:
                    documents.append(doc)
            collections_data[collection_name] = documents
        return collections_data


    async def backup_db(self) -> Response:
        collections_data = await self.export_bson()

        # Create file ZIP in RAM
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for collection_name, documents in collections_data.items():
                bson_bytes = b"".join([bson.BSON.encode(doc) for doc in documents])
                zipf.writestr(f"{collection_name}.bson", bson_bytes)
        zip_buffer.seek(0)

        timestamp = Helper.get_timestamp()
        datetime_str = Helper.timestamp_to_date(ts=timestamp,fmt="%d-%m-%Y_%H_%M_%S",tz="Asia/Ho_Chi_Minh")
        file_name = f"backup_{datetime_str}.zip"

        return Response(content=zip_buffer.getvalue(), media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{file_name}"'})
    
    
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

        result = await logging_crud.search(query, page, limit)
        return result
