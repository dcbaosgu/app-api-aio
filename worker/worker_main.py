import asyncio, sentry_sdk
from worker.sentry.config import *
from worker.rabbitmq.service import rabbitmq_service

sentry_sdk.init(dsn=DSN_SENTRY, environment=ENVIRONMENT, traces_sample_rate=1.0)

async def main():
    
    asyncio.create_task(rabbitmq_service.consumer())

    print("\n[*] Worker is launching...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())