from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

settings = Settings()

SECRET_KEY = settings.SECRET_KEY