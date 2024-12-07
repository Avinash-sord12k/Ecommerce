from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import DB_CONFIGS, Base


class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        host=DB_CONFIGS["host"],
        port=DB_CONFIGS["port"],
        user=DB_CONFIGS["user"],
        password=DB_CONFIGS["password"],
        database=DB_CONFIGS["database"],
    ):
        if hasattr(self, "initialized"):
            err_msg = "DatabaseManager is a singleton class"
            logger.error(err_msg)
            raise Exception(err_msg)

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.initialized = True
        self.engine = None

    def get_url(self, _async: bool = True):
        if not _async:
            return f"postgresql://" f"{self.user}:" f"{self.password}@" f"{self.host}:" f"{self.port}/{self.database}"

        return (
            f"postgresql+asyncpg://"
            f"{self.user}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.database}"
        )

    async def connect(self):
        self.engine = create_async_engine(self.get_url(), pool_size=DB_CONFIGS["pool_size"])
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def disconnect(self):
        await self.engine.dispose()
