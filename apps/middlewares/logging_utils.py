from fastapi import Request
from apps.utils.helper import Helper

# Async generator to reread the response
async def iterate_in_chunks(data: bytes, chunk_size: int = 4096):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


async def get_request_data(request: Request) -> dict:
    data = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None,
    }
    try:
        body_bytes = await request.body()
        data["body"] = body_bytes.decode("utf-8") if body_bytes else None
    except Exception:
        data["body"] = None
    return data


async def get_response_data(response) -> str | None:
    try:
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        response.body_iterator = iterate_in_chunks(body)
        return body.decode("utf-8")
    except Exception:
        return None


async def extract_user_id_from_request(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = await Helper.decode_access_token(token=token)
        return payload.get("uid")
    return None
