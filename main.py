from art import tprint
from core.config import create_app
from core.openapi import custom_openapi
from core.routing import api_routing
from worker.kafka.services import kafka_service
from apps.modules.cronjob.services import scheduler, crons_job


app = create_app()
app.openapi = lambda: custom_openapi(app)
app.include_router(api_routing)

tprint("APP-API-AIO", font="slant")


@app.on_event("startup")
async def startup_event():
    await kafka_service.start_producer()
    await kafka_service.start_consumer()

    scheduler.start()
    await crons_job.add_all_crons()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_service.stop_consumer()
    await kafka_service.stop_producer()
    scheduler.shutdown()
