from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    URL_APPSHEET: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore" 

settings = Settings()

URL_APPSHEET = settings.URL_APPSHEET