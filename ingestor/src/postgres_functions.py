import logging
from dataclasses import asdict

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_upsert
from sqlalchemy.orm import sessionmaker
from src.models import Base, EventModel, EventOrm


class DBEngine:
    def __init__(self, connection_url: str) -> None:
        engine = create_engine(connection_url)
        # Create a session object with binding to sqlalchemy
        session = sessionmaker(bind=engine)()
        logging.info("Connection to Postgres succeeded!")

        # Create tables if not exists based on the defined models
        Base.metadata.create_all(bind=engine)

        # set the session
        self.session = session
        self.engine = engine


def upsert_events(
    db_engine: DBEngine,
    events: list[EventModel],
):
    if len(events) > 0:
        stmt = pg_upsert(EventOrm).values([asdict(event) for event in events])
        stmt = stmt.on_conflict_do_nothing(index_elements=[EventOrm.id])
        db_engine.session.execute(stmt)
        db_engine.session.commit()
