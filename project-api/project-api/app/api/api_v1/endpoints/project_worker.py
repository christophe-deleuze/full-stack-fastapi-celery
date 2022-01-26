# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.celery.async_celery import send_task_and_wait_result, send_task


router = APIRouter()


@router.post("/sleep/")
async def post_sleep(
    time : int
    ) -> Any:
    """ Call project-worker task : sleep """
    
    return await send_task_and_wait_result(
        "sleep", 
        args = (time,), 
        serializer = "json", 
        queue = settings.PROJECT_WORKER_QUEUE)

@router.post("/sleep/async/")
async def post_sleep_async(
    time : int
    ) -> dict:
    """ Call project-worker task : sleep and retrieve task id to get the result later """
    
    return await send_task(
        "sleep", 
        args = (time,), 
        serializer = "json", 
        queue = settings.PROJECT_WORKER_QUEUE)