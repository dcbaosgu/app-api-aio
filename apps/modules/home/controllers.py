import io, zipfile, bson
from fastapi import Response
from .services import HomeService
from apps.utils.helper import Helper

class HomeController:
    def __init__(self):
        self.home_service = HomeService()

    async def export_db(self):

        collections_data = await self.home_service.export_bson()

        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for collection_name, documents in collections_data.items():
                bson_bytes = b"".join([bson.BSON.encode(doc) for doc in documents])
                zipf.writestr(f"{collection_name}.bson", bson_bytes)
        zip_buffer.seek(0)

        timestamp = Helper.get_timestamp()
        datetime = Helper.timestamp_to_date(ts=timestamp, fmt="%d-%m-%Y_%H_%M_%S", tz="Asia/Ho_Chi_Minh")
        
        file_name = f"backup_{datetime}.zip"
        result = Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{file_name}"'}
        )

        return result