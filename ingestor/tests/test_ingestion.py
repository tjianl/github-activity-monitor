from dataclasses import dataclass
from unittest.mock import patch

from src.ingestion import get_first_page, get_paginated_data
from src.models import FirstPage


@dataclass
class MockResponse:
    status_code: int
    json_data: list[dict] = None
    reason: str = None
    headers: dict = None
    links: dict = None

    def json(self):
        return self.json_data

    def raise_for_status(self):
        return None


def test_get_first_page():
    response = MockResponse(
        status_code=200,
        json_data=[{"type": "IssuesEvent"}],
        headers={"X-RateLimit-Limit": 5000, "ETag": "dafadsfsa"},
        links={
            "next": {"url": "https://api.github.com/events?page=2"},
            "last": {"url": "https://api.github.com/events?page=10"},
        },
    )

    with patch("requests.get", return_value=response):
        first_page = get_first_page("https://api.github.com/events", {})

    assert first_page.status_code == 200
    assert first_page.events == [{"type": "IssuesEvent"}]
    assert first_page.poll_interval == 1
    assert first_page.next == "https://api.github.com/events?page=2"


def test_get_first_page_error():
    response = MockResponse(status_code=404)

    with patch("requests.get", return_value=response):
        first_page = get_first_page("https://api.github.com/events", {})

    assert first_page is None


def test_get_paginated_data():
    response_page1 = MockResponse(
        status_code=200,
        json_data=[{"type": "IssuesEvent"}],
        links={"next": {"url": "https://api.github.com/events?page=2"}},
    )
    response_page2 = MockResponse(
        status_code=200,
        json_data=[{"type": "PullRequestEvent"}],
        links={},
    )

    with patch("requests.get") as mock_get:
        mock_get.side_effect = [response_page1, response_page2]
        events = get_paginated_data(FirstPage(status_code=200, next="https://api.github.com/events?page=2"), {}, [])

    assert events == [{"type": "IssuesEvent"}, {"type": "PullRequestEvent"}]
