import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_service import LoggingService
from worker.sentry.config import DSN_SENTRY, ENVIRONMENT


def create_app() -> FastAPI:
    app = FastAPI(
        title="APP-API-AIO",
        version="1.0.0",
        description="RestfulAPI backend with JWT authentication",
    )

    app.add_middleware(LoggingService)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    sentry_sdk.init(
        dsn=DSN_SENTRY,
        environment=ENVIRONMENT,
        traces_sample_rate=1.0,
    )

    return app
