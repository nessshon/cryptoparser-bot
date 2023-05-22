from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from . import models
from .models.base import Base

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = f"{BASE_DIR}/database.sqlite3"


class Database:

    def __init__(self):
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{DB_PATH}",
            pool_pre_ping=True
        )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def run_sync(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    @property
    def channel(self) -> models.Channel:
        return models.Channel(self.sessionmaker)

    @property
    def token(self) -> models.Token:
        return models.Token(self.sessionmaker)

    @property
    def user(self) -> models.User:
        return models.User(self.sessionmaker)
