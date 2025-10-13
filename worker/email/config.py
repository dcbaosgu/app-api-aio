from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    USERNAME_SMTP: str
    PASSWORD_SMTP: str
    HOST_SMTP: str
    PORT_SMTP: int

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

setting = Setting()

USERNAME_SMTP = setting.USERNAME_SMTP
PASSWORD_SMTP = setting.PASSWORD_SMTP
HOST_SMTP = setting.HOST_SMTP
PORT_SMTP = setting.PORT_SMTP