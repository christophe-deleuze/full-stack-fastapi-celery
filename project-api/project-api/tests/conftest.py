# -*- coding: utf-8 -*-

from typing import Generator

import pytest
from httpx import AsyncClient

from api import app


@pytest.fixture(scope="function")
async def async_client() -> Generator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac