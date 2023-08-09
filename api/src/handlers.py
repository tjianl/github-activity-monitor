from datetime import timedelta

from litestar import get
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import (
    get_average_time_between_prs,
    get_num_of_events_per_type,
    get_repositories_more_than_1_pr_event,
)


@get("/repositories")
async def list_repositories(transaction: AsyncSession) -> list[int]:
    repo_ids: list[int] = await get_repositories_more_than_1_pr_event(transaction)
    if repo_ids:
        return [repo_id.repo_id for repo_id in repo_ids]
    else:
        raise NotFoundException(detail="No repositories found with more than 1 Pull Request Event")


@get("/average_time/{repo_id:int}")
async def get_average_time_between_pull_request_events(transaction: AsyncSession, repo_id: int) -> dict[int, int]:
    avg_time: timedelta = await get_average_time_between_prs(transaction, repo_id=repo_id)
    if avg_time:
        return {"repo_id": repo_id, "average_time": avg_time.total_seconds()}
    else:
        raise NotFoundException(
            detail=f"Average time between pull requests with repo_id {repo_id} not found, please use repo_id of returned from /respositories endpoint"
        )


@get("/events_per_type/{offset:int}")
async def get_number_of_events_per_type(transaction: AsyncSession, offset: int) -> list[int]:
    return {
        event_type.event_type: event_type.count
        for event_type in await get_num_of_events_per_type(transaction, offset=offset)
    }
