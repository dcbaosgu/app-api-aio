from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str
    CLAUDE_API_KEY: str

    class Config:
        env_file = "env/app.env"
        extra = "ignore"

setting = Setting()

OPENAI_API_KEY = setting.OPENAI_API_KEY
GEMINI_API_KEY = setting.GEMINI_API_KEY
GEMINI_BASE_URL = setting.GEMINI_BASE_URL
CLAUDE_API_KEY = setting.CLAUDE_API_KEY