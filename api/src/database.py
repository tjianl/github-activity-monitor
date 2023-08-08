from collections.abc import AsyncGenerator

from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.exceptions import ClientException, NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Event
from datetime import timedelta
from src.settings import PostgresSettings


db_config = SQLAlchemyAsyncConfig(connection_string=PostgresSettings().postgres_dsn)


async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


async def get_repositories_more_than_1_pr_event(session: AsyncSession) -> list[Event]:
    query = (
        select(Event.repo_id)
        .where(Event.event_type == "PullRequestEvent", Event.action == "opened")
        .group_by(Event.repo_id)
        .having(func.count() > 1)
        .order_by(func.count().desc())
    )
    result: list[Event] = await session.execute(query)
    try:
        return result
    except NoResultFound as e:
        raise NotFoundException(detail="No repositories found with more than 1 Pull Request Event") from e


async def get_average_time_between_prs(session: AsyncSession, repo_id: int) -> timedelta:
    query = (
        select((func.max(Event.created_at) - func.min(Event.created_at)) / (func.count(1) - 1).label("avg_time"))
        .where(Event.repo_id == repo_id, Event.action == "opened")
        .group_by(Event.repo_id)
    )
    result = await session.execute(query)
    return result.scalar_one()


async def get_num_of_events_per_type(session: AsyncSession, offset: int) -> timedelta:
    query = (
        select(Event.event_type, func.count().label("count"))
        .where(
            Event.created_at.between(func.current_timestamp() - timedelta(minutes=offset), func.current_timestamp())
        )
        .group_by(Event.event_type)
    )
    result = await session.execute(query)
    return result
