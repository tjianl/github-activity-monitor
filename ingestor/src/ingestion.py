import logging
import time

import requests
from src.models import FirstPage
from src.settings import Settings

settings = Settings()


def poll_github_events() -> list[dict]:
    """Polls Github Events API based a calculated interval based on the poll limit, the documentation of the API can be found here:
    https://docs.github.com/en/rest/activity/events
    """
    url: str = "https://api.github.com/events"
    headers: dict[str] = {"Accept": "application/vnd.github+json"}
    events: list = []

    if github_token := settings.github_token:
        headers["Authorization"] = f"Bearer {github_token}"
        logging.info("Polling Github Events API with token, requests limited to 5000 per hour")
    else:
        logging.info("Polling Github Events API without token, requests limited to 60 per hour")

    while True:
        first_page: FirstPage = get_first_page(url=url, headers=headers)
        if first_page.status_code == 200:
            events.extend(first_page.events)
            events: list[dict] = get_paginated_data(response=first_page, headers=headers, events=events)
            yield events

            # Preparing for next poll
            events.clear()
            headers["If-None-Match"] = first_page.etag
            time.sleep(
                max(
                    first_page.poll_interval * first_page.total_pages, settings.max_poll_interval
                )  # Poll dependent on the poll interval limit
            )
        else:
            logging.info(f"Trying again in {settings.max_poll_interval} seconds")
            time.sleep(settings.max_poll_interval)  # Try again later in 60 seconds


def get_first_page(url: str, headers: dict) -> FirstPage:
    try:
        response = requests.get(url, headers=headers, params={"per_page": "100"})
        if response.status_code == 200:
            return FirstPage(
                status_code=response.status_code,
                events=response.json(),
                poll_interval=round(3600 / int(response.headers["X-RateLimit-Limit"])),
                etag=response.headers["ETag"],
                next=response.links.get("next")["url"],
                total_pages=response.links.get("last")["url"][-1],
            )
        else:
            if response.reason == "rate limit exceeded":
                logging.error("Github Events API limit exceeded")
                return FirstPage(status_code=response.status_code)
            else:
                logging.error("Unable to get succesful response")
                response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect: {e}")


def get_paginated_data(response: FirstPage, headers: dict, events: list[dict]) -> list[dict]:
    if response.next:
        next_page_url: str = response.next
        while next_page_url:
            response: requests.models.Response = requests.get(next_page_url, headers=headers)
            if response.status_code == 200:
                events.extend(response.json())
                next_page_url: str | None = response.links["next"]["url"] if response.links.get("next") else None
            elif response.reason == "rate limit exceeded":
                logging.error("Github Events API limit exceeded, writing collected events so far")
                break
            else:
                logging.error("Unable to get succesful response")
                response.raise_for_status()

    return events
