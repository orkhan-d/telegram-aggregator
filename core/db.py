from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from core.settings import settings


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


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
