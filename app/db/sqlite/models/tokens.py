from __future__ import annotations

from datetime import datetime

import pytz
from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import TIME_ZONE
from .base import Base


class Token(Base):
    __tablename__ = "tokens"

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
    name = Column(
        VARCHAR(length=256),
        nullable=False,
    )
    chain = Column(
        VARCHAR(length=256),
        nullable=False,
    )
    links = Column(
        PickleType,
        nullable=True,
    )
    comment = Column(
        VARCHAR(length=1024),
        nullable=True,
    )
    screenshot_link = Column(
        VARCHAR(length=1024),
        nullable=False,
    )
    is_viewed = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.now(tz=pytz.timezone(TIME_ZONE))
    )

    def __init__(self, sessionmaker=None, *args, **kwargs) -> None:
        self.async_sessionmaker: async_sessionmaker = sessionmaker
        super().__init__(*args, **kwargs)

    async def add(self, **kwargs) -> Token:
        async with self.async_sessionmaker() as session:
            model = Token(**kwargs)
            session.add(model)

            await session.commit()
            await session.refresh(model)

            return model

    async def get(self, id_: str | int) -> Token:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Token).
                where(Token.id == id_)
            )
            return query.scalar()

    async def update(self, id_: str | int, **kwargs) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                update(Token).
                where(Token.id == id_).
                values(**kwargs)
            )
            await session.commit()

    async def delete(self, id_: str | int) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                delete(Token).
                where(Token.id == id_)
            )
            await session.commit()

    async def get_all(self) -> list[Token]:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Token)
            )
            return [i[0] for i in query.all()]

    async def get_not_viewed_all(self) -> list[Token]:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(Token).
                where(Token.is_viewed.is_(False)).
                order_by(Token.created_at.desc())
            )
            return [i[0] for i in query.all()]
