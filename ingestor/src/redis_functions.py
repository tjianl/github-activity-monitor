import logging

import redis

from src.utils import camel_to_snake


def connect() -> redis.client.Redis:
    client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    logging.info("Connection to Redis succeeded!")
    return client


def write_events(client: redis.client.Redis, events: list[dict]) -> None:
    for event in events:
        client.json().set(f"{camel_to_snake(event['type'])}:{event['id']}", '$', event)