from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DSN_SENTRY: str
    ENVIRONMENT: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

settings = Settings()

DSN_SENTRY = settings.DSN_SENTRY
ENVIRONMENT = settings.ENVIRONMENT