import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from alembic import context
from src.core.config import settings
from src.infrastructure.database.base import Base

# Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URI)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add the application's models to Alembic's metadata
target_metadata = Base.metadata

# Create async engine
engine = create_async_engine(settings.DATABASE_URI, poolclass=pool.NullPool)


async def run_migrations():
    """Run Alembic migrations asynchronously."""
    async with engine.begin() as connection:  # Mantém a conexão aberta
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: AsyncConnection):
    """Configura e roda as migrações dentro da conexão ativa."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    asyncio.run(run_migrations())


if context.is_offline_mode():
    context.configure(
        url=settings.DATABASE_URI, target_metadata=target_metadata
    )
    context.run_migrations()
else:
    run_migrations_online()
