from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DSN_SENTRY: str
    ENVIRONMENT: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

setting = Setting()

DSN_SENTRY = setting.DSN_SENTRY
ENVIRONMENT = setting.ENVIRONMENT