from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated

from .models import Base
from .config import password, user, database

async_engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@localhost:5432/{database}"
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def lifespan(apps: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]