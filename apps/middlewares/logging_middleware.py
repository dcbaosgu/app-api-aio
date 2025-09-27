from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from apps.middlewares.logging_utils import extract_user_id_from_request, get_request_data, get_response_data
from apps.mongo.base import BaseCRUD
from apps.mongo.engine import engine_logs
from apps.utils.helper import Helper

logs_crud = BaseCRUD("loggings", engine_logs)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = Helper.get_timestamp()

        # Skip endpoints
        skip_paths = ["/docs", "/v1/home/ping"]
        if any(str(request.url).endswith(path) for path in skip_paths):
            return await call_next(request)

        request_data = await get_request_data(request)
        user_id = await extract_user_id_from_request(request)

        response: Response = await call_next(request)
        response_data = await get_response_data(response)

        log_entry = {
            "user_id": user_id,
            "request": request_data,
            "response": {
                "status_code": response.status_code,
                "body": response_data,
            },
            "process_time": round((Helper.get_timestamp() - start_time) * 1000, 2),
        }

        try:
            await logs_crud.create(log_entry)
        except Exception as e:
            print("⚠️ Error saving log:", e)

        return response
