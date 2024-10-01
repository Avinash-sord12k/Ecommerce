from __future__ import annotations

from asyncpg import create_pool
from loguru import logger
from sqlalchemy.engine import create_engine


class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port, user, password, database, base):
        if hasattr(self, "initialized"):
            err_msg = "DatabaseManager is a singleton class"
            logger.error(err_msg)
            raise Exception(err_msg)

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool = None
        self.connection = None
        self.cursor = None
        self.transaction = None
        self.initialized = True
        self.engine = create_engine(self.get_url(), future=True)
        base.metadata.create_all(self.engine)

    def get_url(self):
        return (
            f"postgresql://"
            f"{self.user}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.database}"
        )

    async def connect(self):
        self.pool = await create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        async with self.pool.acquire() as connection:
            result = await connection.fetch("SELECT NOW();")
            logger.info(f"Current date and time: {result[0]['now']}")

    async def disconnect(self):
        if self.transaction is not None:
            logger.debug("Rolling back transaction")
            await self.transaction.rollback()
        if self.connection is not None:
            logger.debug("Closing connection")
            await self.connection.close()
        if self.pool is not None:
            logger.debug("Closing pool")
            await self.pool.close()

    async def execute(self, query, args=None):
        if args is None:
            args = []
        await self.cursor.execute(query, args)
        await self.connection.commit()

    async def fetchone(self, query, args=None):
        if args is None:
            args = []
        await self.cursor.execute(query, args)
        return await self.cursor.fetchone()

    async def fetchall(self, query, args=None):
        if args is None:
            args = []
        await self.cursor.execute(query, args)
        return await self.cursor.fetchall()
