from datetime import datetime
from typing import Optional

from pydantic.dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger


# Pydantic dataclasses
@dataclass
class FirstPage:
    status_code: int
    events: Optional[list] = None
    poll_interval: Optional[int] = None
    etag: Optional[str] = None
    next: Optional[str] = None
    total_pages: Optional[int] = None


@dataclass
class EventModel:
    id: int
    event_type: str
    created_at: datetime
    actor_id: int
    repo_id: int
    action: str


# SQLAlchemy ORM models
class Base(DeclarativeBase):
    pass


class EventOrm(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    event_type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    actor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    repo_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
