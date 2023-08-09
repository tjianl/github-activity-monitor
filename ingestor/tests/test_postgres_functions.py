import pytest
from src.models import EventModel, EventOrm
from src.postgres_functions import DBEngine, upsert_events


@pytest.fixture()
def events():
    return [
        EventModel(
            id=30924443268,
            event_type="IssuesEvent",
            created_at="2023-08-06T10:06:07Z",
            actor_id=101969092,
            repo_id=41889031,
            action="opened",
        ),
        EventModel(
            id=30924443273,
            event_type="WatchEvent",
            created_at="2023-08-06T10:06:07Z",
            actor_id=25137893,
            repo_id=566639549,
            action="started",
        ),
        EventModel(
            id=30924443248,
            event_type="PullRequestEvent",
            created_at="2023-08-06T10:06:07Z",
            actor_id=39814207,
            repo_id=531755904,
            action="opened",
        ),
    ]


def test_upsert_events(db_engine: DBEngine, events: list[EventModel]):
    upsert_events(db_engine, events)
    assert db_engine.session.query(EventOrm).count() == 3


def test_upsert_events_conflict(db_engine: DBEngine):
    events = [
        EventModel(
            id=30924443268,
            event_type="IssuesEvent",
            created_at="2023-08-06T10:06:07Z",
            actor_id=101969092,
            repo_id=41889031,
            action="opened",
        )
    ]
    upsert_events(db_engine, events)
    assert db_engine.session.query(EventOrm).count() == 3
