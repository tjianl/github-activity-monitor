from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.engine import URL
from typing import Optional


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")

    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = ""
    database: str = "postgres"
    postgres_dsn: Optional[URL] = None

    def model_post_init(self, __context: Any) -> None:
        self.postgres_dsn: URL = URL.create(
            "postgresql",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            # query={
            #     "sslmode": "require"
            # },
        )

        return super().model_post_init(__context)


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")

    host: str = "localhost"
    port: int = 6379


class Settings(BaseSettings):
    github_token: Optional[str] = None
    max_poll_interval: int = 10  # In seconds
