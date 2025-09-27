from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAY: int = 3
    REMEMBER_TOKEN_DAY: int = 30

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

settings = Settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAY = settings.ACCESS_TOKEN_EXPIRE_DAY
REMEMBER_TOKEN_DAY = settings.REMEMBER_TOKEN_DAY