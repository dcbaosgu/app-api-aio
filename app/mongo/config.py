from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_AIO_NAME: str
    DATABASE_LOG_NAME: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

setting = Setting()

AIO_DATABASE_NAME = setting.DATABASE_AIO_NAME
LOG_DATABASE_NAME = setting.DATABASE_LOG_NAME