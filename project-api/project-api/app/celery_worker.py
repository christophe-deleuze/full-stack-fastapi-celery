# -*- coding: utf-8 -*-

from typing import List

from celery.result import AsyncResult

from app.core.config import settings
from app.core.celery.async_celery import send_task


async def send_task_integer_multiplication(
        integer: int
) -> AsyncResult:
    """ Send task : integer-multiplication, to project-worker """

    return await send_task(
        "integer-multiplication",
        args=(integer,),
        serializer="json",
        queue=settings.PROJECT_WORKER_QUEUE)


async def send_task_integers_sum(
        integers: List[int]
) -> AsyncResult:
    """ Send task : integers-sum, to project-worker """

    return await send_task(
        "integers-sum",
        args=(integers,),
        serializer="json",
        queue=settings.PROJECT_WORKER_QUEUE)
