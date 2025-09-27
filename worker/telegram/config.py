from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_ID: str
    ENVIRONMENT: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

settings = Settings()

BOT_TOKEN = settings.BOT_TOKEN
CHANNEL_ID = settings.CHANNEL_ID
ENVIRONMENT = settings.ENVIRONMENT