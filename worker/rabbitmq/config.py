from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RABBITMQ_URL: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

settings = Settings()

RABBITMQ_URL = settings.RABBITMQ_URL