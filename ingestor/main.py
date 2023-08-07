import logging
import sys

import typer
from typing_extensions import Annotated


from src import service
from src.ingestion import poll_github_events
from src.redis_functions import connect, write_events
from src.postgres_functions import DBEngine, create_connection_url, upsert_events

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s [%(levelname)8s] %(message)s")


def main(db_client: Annotated[str, typer.Argument] = "postgres"):
    if db_client == "postgres":
        db_connection: DBEngine = DBEngine(
            connection_url=create_connection_url(
                username="postgres",
                password="tjian123",
                server="localhost",
                port=5432,
                database="postgres",
            )
        )

    elif db_client == "redis":
        db_connection = connect()

    events_gen = poll_github_events()

    for events in events_gen:
        logging.info(f"Returned {len(events)}")
        if db_client == "postgres":
            upsert_events(db_engine=db_connection, events=service.parse_events(events))
        elif db_client == "redis":
            write_events(client=db_connection, events=service.parse_events_redis(events))


if __name__ == "__main__":
    typer.run(main)
