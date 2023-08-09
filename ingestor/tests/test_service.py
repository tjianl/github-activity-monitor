import json
from pathlib import Path

import pytest
from src.models import EventModel
from src.service import parse_events


@pytest.fixture
def events() -> list[dict]:
    with open(Path(__file__).parent / "test_response.json") as f:
        data = json.load(f)
    return data


def test_parse_events(events: list[dict]):
    parsed_events: list[EventModel] = parse_events(events)
    assert len(parsed_events) == 3

    assert parsed_events[0] == EventModel(
        id=30924443268,
        event_type="IssuesEvent",
        created_at="2023-08-06T10:06:07Z",
        actor_id=101969092,
        repo_id=41889031,
        action="opened",
    )

    assert parsed_events[1] == EventModel(
        id=30924443273,
        event_type="WatchEvent",
        created_at="2023-08-06T10:06:07Z",
        actor_id=25137893,
        repo_id=566639549,
        action="started",
    )

    assert parsed_events[2] == EventModel(
        id=30924443248,
        event_type="PullRequestEvent",
        created_at="2023-08-06T10:06:07Z",
        actor_id=39814207,
        repo_id=531755904,
        action="opened",
    )
