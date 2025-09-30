from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USERNAME_SMTP: str
    PASSWORD_SMTP: str
    HOST_SMTP: str
    PORT_SMTP: int

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

settings = Settings()

USERNAME_SMTP = settings.USERNAME_SMTP
PASSWORD_SMTP = settings.PASSWORD_SMTP
HOST_SMTP = settings.HOST_SMTP
PORT_SMTP = settings.PORT_SMTP