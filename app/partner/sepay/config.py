from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    VIRTUAL_ACCOUNT: str
    BANK_NAME: str
    SEPAY_API_KEY: str

    class Config:
        env_file = "env/partner.env"
        extra = "ignore"

setting = Setting()

VIRTUAL_ACCOUNT = setting.VIRTUAL_ACCOUNT
BANK_NAME = setting.BANK_NAME
SEPAY_API_KEY = setting.SEPAY_API_KEY