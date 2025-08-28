from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import MetaData, text, func
from core.settings import settings

from datetime import datetime as dt, UTC
from uuid import UUID


DATABASE_URL = settings.db.url
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s',
}


class UuidPkMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True,
                                     server_default=text('gen_random_uuid()'))


class TimestampsMixin:
    created_at: Mapped[dt] = mapped_column(
        default=lambda: dt.now(UTC),
        nullable=False
    )
    updated_at: Mapped[dt] = mapped_column(
        default=lambda: dt.now(UTC),
        onupdate=lambda: dt.now(UTC),
        nullable=False
    )


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
