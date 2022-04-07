# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
