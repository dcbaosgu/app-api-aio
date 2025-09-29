import httpx
import requests
import asyncio

URL = "http://127.0.0.1:8000/v1/home/ping"
TOKEN = "YOUR_BEARER_TOKEN"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# --- Synchronous requests ---
def ping_requests():
    response = requests.get(URL, headers=HEADERS)
    print("=== requests (synchronous) ===")
    print("Status:", response.status_code)
    print("Headers:", dict(response.headers))
    print("JSON:", response.json())
    return response.json()

# --- Synchronous httpx ---
def ping_httpx_sync():
    response = httpx.get(URL, headers=HEADERS)
    print("=== httpx (synchronous) ===")
    print("Status:", response.status_code)
    print("Headers:", dict(response.headers))
    print("JSON:", response.json())
    return response.json()

# --- Async httpx ---
async def ping_httpx_async():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL, headers=HEADERS)
    print("=== httpx (asynchronous) ===")
    print("Status:", response.status_code)
    print("Headers:", dict(response.headers))
    print("JSON:", response.json())
    return response.json()

if __name__ == "__main__":
    ping_requests()
    ping_httpx_sync()
    asyncio.run(ping_httpx_async())
