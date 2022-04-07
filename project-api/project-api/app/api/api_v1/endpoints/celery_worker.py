# -*- coding: utf-8 -*-

from typing import List

from fastapi import APIRouter, Query

from app.core.celery.schemas import AsyncTask
from app.core.celery.responses import task_sync_response, task_async_response
from app.celery_worker import send_task_integers_sum, send_task_integer_multiplication

router = APIRouter()


@router.post("/integer-multiplication/")
async def post_integer_multiplication(
        integer: int = Query(
            ...,
            description="Integer to multiply by 2.")
) -> int:
    """ Send task : integer-multiplication, to project-worker and wait for the result """

    async_result = await send_task_integer_multiplication(integer)
    return await task_sync_response(async_result)


@router.post("/integer-multiplication/async/", response_model=AsyncTask)
async def post_integer_multiplication_async(
        integer: int = Query(
            ...,
            description="Integer to multiply by 2.")
) -> dict[str, str]:
    """ Send task : integer-multiplication, to project-worker and retrieve taskId to get the result later """

    async_result = await send_task_integer_multiplication(integer)
    return await task_async_response(async_result)


@router.post("/integers-sum/")
async def post_integers_sum(
        integers: List[int] = Query(
            ...,
            description="List of integers to sum.")
) -> int:
    """ Send task : integers-sum, to project-worker and wait for the result """

    async_result = await send_task_integers_sum(integers)
    return await task_sync_response(async_result)


@router.post("/integers-sum/async/", response_model=AsyncTask)
async def post_integers_sum_async(
        integers: List[int] = Query(
            ...,
            description="List of integers to sum.")
) -> dict[str, str]:
    """ Send task : integers-sum, to project-worker and retrieve taskId to get the result later """

    async_result = await send_task_integers_sum(integers)
    return await task_async_response(async_result)
