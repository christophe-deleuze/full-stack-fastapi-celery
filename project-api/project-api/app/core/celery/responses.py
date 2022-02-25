# -*- coding: utf-8 -*-

from typing import Any

from celery.result import AsyncResult

from app.core.config import settings
from app.core.celery.schemas import AsyncTask
from app.core.celery.async_celery import task_ready, task_result


async def task_sync_response(
    async_result: AsyncResult, 
    celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT, 
    celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT) -> Any:
    """ Wait until task is ready then return the result """
    
    # Await until task is ready or timeout
    await task_ready(
        async_result, 
        celery_task_ready_time_out = celery_task_ready_time_out)
    
    # Await until task result retrieve
    result = await task_result(
        async_result, 
        celery_task_result_time_out = celery_task_result_time_out)
    
    return result

async def task_async_response(async_result: AsyncResult) -> AsyncTask:
    """ Return the taskId of a task """
    
    # Return  Celery AsyncResult id
    return {"taskId": async_result.id}