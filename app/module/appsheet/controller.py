from .service import appsheet_service


class AppSheetController:
    def __init__(self):
        self.service = appsheet_service

    async def send_report(self, data: dict):
        result = await self.service.send_report(data)
        return result

    async def fetch_report(self, page: int, limit: int):
        result =  await self.service.fetch_report(page, limit)
        return result