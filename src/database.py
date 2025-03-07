from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import settings

Base = declarative_base()

metadata = MetaData()

engine = create_async_engine(settings.db_url, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Database:
    @staticmethod
    async def create_tables() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_async_session(commit: bool = False):
        async with async_session_maker() as session:
            session: AsyncSession
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    async def get_session_without_commit(cls):
        async for session in cls.get_async_session(commit=False):
            yield session

    @classmethod
    async def get_session_with_commit(cls):
        async for session in cls.get_async_session(commit=True):
            yield session


db = Database()

SessionWithCommit = Annotated[
    AsyncSession, Depends(db.get_session_with_commit)
]
SessionWithoutCommit = Annotated[
    AsyncSession, Depends(db.get_session_without_commit)
]
