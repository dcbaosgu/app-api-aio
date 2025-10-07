from fastapi import APIRouter

from apps.modules.home.routers import router as home_router
from apps.modules.user.routers import router as user_router
from apps.modules.product.routers import router as product_router
from apps.modules.account.router import router as account_router
from apps.modules.agent.routers import router as agent_router
from apps.modules.appsheet.routers import router as appsheet_router
from apps.modules.invoices.routers import router as invoice_router
from apps.modules.forum.routers import router as forum_router
from apps.modules.festival.routers import router as festival_router
from apps.modules.taxcode.routers import router as taxcode_router
from apps.modules.socket.routers import router as socket_router
from apps.modules.cronjob.routers import router as cron_router
from apps.modules.redis.routers import router as redis_router
from apps.modules.stream.routers import router as stream_router
from apps.modules.news.routers import router as news_router
from worker.sentry.routers import router as sentry_router

api_router = APIRouter()

api_router.include_router(home_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(account_router)
api_router.include_router(agent_router)
api_router.include_router(appsheet_router)
api_router.include_router(invoice_router)
api_router.include_router(forum_router)
api_router.include_router(festival_router)
api_router.include_router(taxcode_router)
api_router.include_router(socket_router)
api_router.include_router(cron_router)
api_router.include_router(redis_router)
api_router.include_router(stream_router)
api_router.include_router(news_router)
api_router.include_router(sentry_router)
