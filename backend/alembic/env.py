import asyncio
import os
import sys

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Base  # noqa: E402

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(
        config.get_main_option('sqlalchemy.url'),
        poolclass=pool.NullPool,
        future=True,
        echo=False,
    )

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
