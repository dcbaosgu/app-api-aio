from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_LOGS_NAME: str
    DATABASE_TRACKING_NAME: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

settings = Settings()

AIO_DATABASE_NAME = settings.DATABASE_NAME
LOGS_DATABASE_NAME = settings.DATABASE_LOGS_NAME
TRACKING_DATABASE_NAME = settings.DATABASE_TRACKING_NAME