from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_CHAT_TOPIC: str
    KAFKA_CHAT_GROUP: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

settings = Settings()

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
KAFKA_CHAT_TOPIC = settings.KAFKA_CHAT_TOPIC
KAFKA_CHAT_GROUP = settings.KAFKA_CHAT_GROUP