from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from configs.environment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()

# Generate Database URL
DATABASE_URL = f"{env.DATABASE_DIALECT}://" \
               f"{env.DATABASE_USERNAME}:" \
               f"{env.DATABASE_PASSWORD}@" \
               f"{env.DATABASE_HOST}:{env.DATABASE_PORT}/" \
               f"{env.DATABASE_NAME}"

# Create Database Engine
engine = create_async_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


async def get_session() -> AsyncSession:
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
