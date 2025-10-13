from fastapi import APIRouter

from app.module.home.router import router as home_router
from app.module.user.router import router as user_router
from app.module.product.router import router as product_router
from app.module.account.router import router as account_router
from app.module.agent.router import router as agent_router
from app.module.appsheet.router import router as appsheet_router
from app.module.invoice.router import router as invoice_router
from app.module.forum.router import router as forum_router
from app.module.festival.router import router as festival_router
from app.module.taxcode.router import router as taxcode_router
from app.module.socket.router import router as socket_router
from app.module.cronjob.router import router as cron_router
from app.module.redis.router import router as redis_router
from app.module.stream.router import router as stream_router
from app.module.news.router import router as news_router
from app.module.apikey.router import router as api_router
from worker.sentry.router import router as sentry_router

api_routing = APIRouter()

api_routing.include_router(home_router)
api_routing.include_router(user_router)
api_routing.include_router(product_router)
api_routing.include_router(account_router)
api_routing.include_router(agent_router)
api_routing.include_router(appsheet_router)
api_routing.include_router(invoice_router)
api_routing.include_router(forum_router)
api_routing.include_router(festival_router)
api_routing.include_router(taxcode_router)
api_routing.include_router(socket_router)
api_routing.include_router(cron_router)
api_routing.include_router(redis_router)
api_routing.include_router(stream_router)
api_routing.include_router(news_router)
api_routing.include_router(api_router)
api_routing.include_router(sentry_router)
