import json
from typing import Any, Mapping

from sqlalchemy.sql import text

from sqlalchemy.ext.asyncio import create_async_engine


class DbClient:
    def __init__(self, user: str, password: str, host: str, port: int, database: str, debug: bool = False):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
            echo=True
        )
        self.debug = debug

    async def query(self, query: str, variables=None) -> Any:
        async with self.engine.begin() as conn:
            if self.debug:
                print(f"{query=}, {variables=}")
            result = await conn.execute(text(query), parameters=variables)
            return result

    @classmethod
    def prod(cls, debug: bool = False) -> 'DbClient':
        with open("secrets/db.json", "r") as f:
            return DbClient(**(json.loads(f.read()) | {'debug': debug}))
