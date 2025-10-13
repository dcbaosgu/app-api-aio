from .schema import Response
from .service import sentry_service
from worker.telegram.service import sentry_bot


class SentryController:
    def __init__(self) -> None:
        self.service = sentry_service
        
    async def capture_issues(self, data: dict) -> Response:
        result = await self.service.parse(data)
        await sentry_bot.send_telegram(result)
        # print("[SENTRY-WEBHOOK]", result)
        return result
