from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

    @property
    def REDIS_URL(self):
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

settings = Settings()

REDIS_URL = settings.REDIS_URL