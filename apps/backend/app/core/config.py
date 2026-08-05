"""
FastAPI Core Configuration Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change_this_to_a_secure_256bit_random_secret_in_production"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database & Pooling Configuration
    DATABASE_URL: str = (
        "postgresql+asyncpg://alphamind:alphamind_dev_pass@localhost:5432/alphamind_db"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_PRE_PING: bool = True
    DB_PGBOUNCER_MODE: bool = False
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_STREAM_NAME: str = "alphamind:events:stream"
    REDIS_STREAM_MAXLEN: int = 10000
    REDIS_CONSUMER_GROUP: str = "alphamind-event-consumers"
    REDIS_CONSUMER_NAME: str = "worker-01"
    REDIS_ENABLE_STREAMS: bool = True
    REDIS_ENABLE_PUBSUB: bool = True
    REDIS_PUBSUB_CHANNEL: str = "alphamind:sse:events"
    SSE_HEARTBEAT_INTERVAL: int = 15
    SSE_RECONNECT_DELAY: int = 3
    SSE_MAX_CLIENTS_PER_WORKER: int = 1000

    # External APIs
    POLYGON_API_KEY: str = ""
    FRED_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def validate_environment_secrets(self) -> None:
        """Enforce secret key safety in staging and production environments."""
        if self.ENVIRONMENT.lower() in ("staging", "production"):
            if (
                self.SECRET_KEY == "change_this_to_a_secure_256bit_random_secret_in_production"
                or len(self.SECRET_KEY) < 32
            ):
                raise RuntimeError(
                    "CRITICAL SECURITY ERROR: Staging/Production environment detected with default or insecure SECRET_KEY. Refusing to start."
                )


settings = Settings()
settings.validate_environment_secrets()
