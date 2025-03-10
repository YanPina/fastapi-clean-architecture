import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.base import get_db


@pytest.mark.asyncio
async def test_get_db():
    """Test that get_db() correctly yields an AsyncSession."""
    db_generator = get_db()
    session = await anext(db_generator)

    assert isinstance(session, AsyncSession)

    await db_generator.aclose()
