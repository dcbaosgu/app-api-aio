from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    SECRET_KEY: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

setting = Setting()

SECRET_KEY = setting.SECRET_KEY