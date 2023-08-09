import logging
import sys

import typer
from typing_extensions import Annotated


from src import service
from src.ingestion import poll_github_events
from src.redis_functions import connect_redis, write_events
from src.postgres_functions import DBEngine, upsert_events
from src.settings import PostgresSettings, RedisSettings
from redis.client import Redis

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s [%(levelname)8s] %(message)s")


def main(db_client: Annotated[str, typer.Argument] = "postgres"):
    if db_client == "postgres":
        db_connection: DBEngine = DBEngine(connection_url=PostgresSettings().postgres_dsn)

    elif db_client == "redis":
        redis_settings = RedisSettings()
        db_connection: Redis = connect_redis(host=redis_settings.host, )

    events_gen = poll_github_events()

    for events in events_gen:
        logging.info(f"Polled {len(events)} Github Events")
        if db_client == "postgres":
            upsert_events(db_engine=db_connection, events=service.parse_events(events))
        elif db_client == "redis":
            write_events(client=db_connection, events=service.parse_events_redis(events))


if __name__ == "__main__":
    typer.run(main)
