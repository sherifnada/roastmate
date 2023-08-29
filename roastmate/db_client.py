import json
from typing import Any

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine


class DbClient:
    def __init__(self, user: str, password: str, host: str, port: int, database: str):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
            echo=True
        )

    async def query(self, query: str) -> Any:
        async with self.engine.begin() as conn:
            result = await conn.execute(text("SELECT 1;"))
            return result.fetchall()

    @classmethod
    def prod(cls) -> 'DbClient':
        with open("secrets/db.json", "r") as f:
            return DbClient(**json.loads(f.read()))
