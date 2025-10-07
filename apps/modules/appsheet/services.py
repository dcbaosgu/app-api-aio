import requests
from .config import URL_APPSHEET
from apps.utils.helper import Helper

class AppSheetService:
    def __init__(self):
        self.url = URL_APPSHEET
        
    async def send_report(self, data: dict) -> dict:
        if "create_time" in data and data["create_time"]:
            data["create_time"] = Helper.timestamp_to_date(ts=data["create_time"], tz="Asia/Ho_Chi_Minh")
        try:
            response = requests.post(self.url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def fetch_report(self, page: int, limit: int) -> dict:
        try:
            params = {"page": page, "limit": limit}
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}