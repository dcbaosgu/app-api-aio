from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware.logging_util import *
from app.mongo.engine import engine_log
from app.mongo.base import BaseCRUD
from app.utils.helper import Helper

logs_crud = BaseCRUD("logging", engine_log)

class LoggingService(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = Helper.get_timestamp()

        skip_paths = ["/docs", "/redoc", "/v1/home/ping", "/openapi.json"]
        if any(str(request.url).endswith(path) for path in skip_paths):
            return await call_next(request)

        request_data = await get_request_data(request)
        user_id = await extract_user_id_from_request(request)

        response: Response = await call_next(request)
        response_data = await get_response_data(response)

        """ Write full logs no limit -> High memory
        log_entry = {
            "user_id": user_id,
            "request": request_data,
            "response": {
                "status_code": response.status_code,
                "body": response_data,
            },
            "process_time": round((Helper.get_timestamp() - start_time) * 1000, 2),
        }"""
        
        log_data = {
            "user_id": user_id,
            "request": {
                "method": request_data.get("method"),
                "url": request_data.get("url"),
                "body": request_data.get("body"),
            },
            "response": {
                "status_code": response.status_code,
                "body": response_data,
            },
            "config": {
                "client": request_data.get("client"),
                "platform": request_data.get("headers", {}).get("sec-ch-ua-platform"),
                "environment": request_data.get("headers", {}).get("user-agent"),
                "browser": request_data.get("headers", {}).get("sec-ch-ua"),
            },
            "process_time": round((Helper.get_timestamp() - start_time) * 1000, 2),
            "created_at": Helper.get_timestamp()
        }

        try:
            await logs_crud.create(log_data)
        except Exception as e:
            print("[LOGGING] Error saving log:", e)

        return response
