from sqlalchemy import func, select


class BaseRepository:
    def __init__(self, db):
        self.db = db

    async def get_paginated(
        self, query, page: int = 1, page_size: int = 10
    ) -> tuple[list[dict], int]:
        async with self.db.engine.begin() as connection:
            count_query = select(func.count()).select_from(query.subquery())
            total = await connection.scalar(count_query)

            offset = (page - 1) * page_size
            paginated_query = query.offset(offset).limit(page_size)
            result = await connection.execute(paginated_query)
            items = result.fetchall()

            return [item._asdict() for item in items], total
