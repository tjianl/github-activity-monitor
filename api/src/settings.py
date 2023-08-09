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
            "postgresql+asyncpg",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

        return super().model_post_init(__context)
