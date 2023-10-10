from __future__ import annotations

from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker

from ._base import Base


class Channel(Base):
    __tablename__ = "channels"

    pk = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    id = Column(
        BigInteger,
        unique=True,
        nullable=False,
    )
    title = Column(
        VARCHAR(length=256),
        nullable=False,
    )
    language_code = Column(
        VARCHAR(5),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=func.now()
    )

    def __init__(self, sessionmaker=None, *args, **kwargs) -> None:
        self.async_sessionmaker: async_sessionmaker = sessionmaker
        super().__init__(*args, **kwargs)

    async def add(self, **kwargs) -> None:
        async with self.async_sessionmaker() as session:
            session.add(Channel(**kwargs))
            await session.commit()

    async def get(self, id_: str | int) -> Channel:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Channel).
                where(Channel.id == id_)
            )
            return query.scalar()

    async def update(self, id_: str | int, **kwargs) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                update(Channel).
                where(Channel.id == id_).
                values(**kwargs)
            )
            await session.commit()

    async def delete(self, id_: str | int) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                delete(Channel).
                where(Channel.id == id_)
            )
            await session.commit()

    async def get_all(self) -> list[Channel]:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Channel)
            )
            return [i[0] for i in query.all()]

    async def is_exists(self, id_: str | int) -> bool:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Channel).
                where(Channel.id == id_)
            )
            return query.scalar() is not None
