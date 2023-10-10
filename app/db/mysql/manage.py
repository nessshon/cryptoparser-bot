from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from . import models
from ...config import DatabaseConfig


class Database:
    """
    Database manager for handling database connections and operations.
    """

    def __init__(self, config: DatabaseConfig) -> None:
        """
        Initialize the Database manager.

        :param config: The database configuration object.
        """
        self.engine = create_async_engine(
            url=config.url(),
            pool_pre_ping=True,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init(self) -> 'Database':
        """
        Initialize the database.

        :return: The initialized Database instance.
        """
        async with self.engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.create_all)
        return self

    async def close(self) -> None:
        """
        Close the database connection.
        """
        await self.engine.dispose()

    @property
    def channel(self) -> models.Channel:
        return models.Channel(self.session)

    @property
    def token(self) -> models.Token:
        return models.Token(self.session)

    @property
    def user(self) -> models.User:
        return models.User(self.session)
