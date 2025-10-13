from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_ID: str
    ENVIRONMENT: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

setting = Setting()

BOT_TOKEN = setting.BOT_TOKEN
CHANNEL_ID = setting.CHANNEL_ID
ENVIRONMENT = setting.ENVIRONMENT