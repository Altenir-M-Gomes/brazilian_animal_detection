from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from configs.database import Session

async def getSession() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
