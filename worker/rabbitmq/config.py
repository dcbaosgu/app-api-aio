from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    RABBITMQ_URL: str
    RABBITMQ_QUEUE: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

setting = Setting()

RABBITMQ_URL = setting.RABBITMQ_URL
RABBITMQ_QUEUE = setting.RABBITMQ_QUEUE