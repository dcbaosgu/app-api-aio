from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    VIRTUAL_ACCOUNT: str
    BANK_NAME: str

    class Config:
        env_file = "env/partner.env"
        extra = "ignore"

setting = Setting()

VIRTUAL_ACCOUNT = setting.VIRTUAL_ACCOUNT
BANK_NAME = setting.BANK_NAME