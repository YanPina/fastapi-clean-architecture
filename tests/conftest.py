import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.infrastructure.database.base import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
TEST_DB_FILE = "test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

TestSession = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSession() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSession() as session:
        yield session

@pytest.fixture(autouse=True)
async def clean_database(db_session: AsyncSession):
    """Clear database before each test to prevent duplicate users."""
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()
