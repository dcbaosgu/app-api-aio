import asyncio, sentry_sdk
from worker.sentry.config import *
from worker.rabbitmq.services import RabbitMQServices

sentry_sdk.init(dsn=DSN_SENTRY, environment=ENVIRONMENT, traces_sample_rate=1.0)

async def main():
    rabbit = RabbitMQServices()
    asyncio.create_task(rabbit.consumer())

    print("\n[*] Worker is launching...")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())