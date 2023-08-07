from dataclasses import asdict

from src.models import EventModel


def parse_events(events: list[dict]):
    parsed_events: list[EventModel] = []
    for event in events:
        if event["type"] in ["PullRequestEvent", "WatchEvent", "IssuesEvent"]:
            parsed_events.append(
                asdict(
                    EventModel(
                        id=event["id"],
                        event_type=event["type"],
                        created_at=event["created_at"],
                        actor_id=event["actor"]["id"],
                        repo_id=event["repo"]["id"],
                        action=event["payload"]["action"],
                    )
                )
            )

    return parsed_events


def parse_events_redis(events: list[dict]) -> list[dict]:
    return [event for event in events if event["type"] in ["PullRequestEvent", "WatchEvent", "IssuesEvent"]]
