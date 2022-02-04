# -*- coding: utf-8 -*-

from typing import Any, List

from fastapi import APIRouter, Query


from app.celery.schemas import AsyncTask
from app.celery.async_celery import task_result
from app.project_worker import send_task_integer_multiplication, send_task_integers_sum


router = APIRouter()


@router.post("/integer-multiplication/")
async def post_integer_multiplication(
    integer : int = Query(None, description="Integer to multiply by 2.")
    ) -> Any:
    """ Send task : integer-multiplication, to project-worker and wait for the result """
    
    async_result = await send_task_integer_multiplication(integer)
    return await task_result(async_result)

@router.post("/integer-multiplication/async/", response_model = AsyncTask)
async def post_integer_multiplication_async(
    integer : int = Query(None, description="Integer to multiply by 2.")
    ) -> Any:
    """ Send task : integer-multiplication, to project-worker and retrieve taskId to get the result later """
    
    async_result = await send_task_integer_multiplication(integer)
    return {"taskId": async_result.id}

@router.post("/integers-sum/")
async def post_integers_sum(
    integers : List[int] = Query(None, description="List of integers to sum.")
    ) -> Any:
    """ Send task : integers-sum, to project-worker and wait for the result """
    
    async_result = await send_task_integers_sum(integers)
    return await task_result(async_result)

@router.post("/integers-sum/async/", response_model = AsyncTask)
async def post_integers_sum_async(
    integers : List[int] = Query(None, description="List of integers to sum.")
    ) -> Any:
    """ Send task : integers-sum, to project-worker and retrieve taskId to get the result later """
    
    async_result = await send_task_integers_sum(integers)
    return {"taskId": async_result.id}