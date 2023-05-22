from __future__ import annotations

from datetime import datetime

import pytz
from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import TIME_ZONE
from .base import Base


class User(Base):
    __tablename__ = "users"

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
    first_name = Column(
        VARCHAR(length=64),
        nullable=False,
    )
    is_admin = Column(
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

    async def add(self, **kwargs) -> User:
        async with self.async_sessionmaker() as session:
            model = User(**kwargs)
            session.add(model)

            await session.commit()
            await session.refresh(model)

            return model

    async def get(self, id_: str | int) -> User:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(User).
                where(User.id == id_)
            )
        return query.scalar()

    async def update(self, id_: str | int, **kwargs) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                update(User).
                where(User.id == id_).
                values(**kwargs)
            )
            await session.commit()

    async def delete(self, id_: str | int) -> None:
        async with self.async_sessionmaker() as session:
            await session.execute(
                delete(User).
                where(User.id == id_)
            )
            await session.commit()

    async def is_exists(self, user_id: str | int) -> bool:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(User.id).
                where(User.id == user_id)
            )
            return query.scalar() is not None

    async def get_all_admins(self) -> list[User]:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(User).
                where(User.is_admin.is_(True)).
                order_by(User.created_at.desc())
            )
            return [i[0] for i in query.all()]

    async def get_all(self) -> list[User]:
        async with self.async_sessionmaker() as session:
            query = await session.execute(
                select(User)
            )
            return [i[0] for i in query.all()]
