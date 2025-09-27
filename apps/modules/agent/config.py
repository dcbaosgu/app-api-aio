from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

settings : Settings = Settings()

OPENAI_API_KEY = settings.OPENAI_API_KEY
GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_BASE_URL = settings.GEMINI_BASE_URL