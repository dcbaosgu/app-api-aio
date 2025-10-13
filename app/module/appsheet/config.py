from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    URL_APPSHEET: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore" 

setting = Setting()

URL_APPSHEET = setting.URL_APPSHEET