from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_CHAT_TOPIC: str
    KAFKA_CHAT_GROUP: str

    class Config:
        env_file = "env/worker.env"
        extra = "ignore"

setting = Setting()

KAFKA_BOOTSTRAP_SERVERS = setting.KAFKA_BOOTSTRAP_SERVERS
KAFKA_CHAT_TOPIC = setting.KAFKA_CHAT_TOPIC
KAFKA_CHAT_GROUP = setting.KAFKA_CHAT_GROUP