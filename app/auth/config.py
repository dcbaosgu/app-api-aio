from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAY: int = 3
    REMEMBER_TOKEN_DAY: int = 30

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

setting = Setting()

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAY = setting.ACCESS_TOKEN_EXPIRE_DAY
REMEMBER_TOKEN_DAY = setting.REMEMBER_TOKEN_DAY