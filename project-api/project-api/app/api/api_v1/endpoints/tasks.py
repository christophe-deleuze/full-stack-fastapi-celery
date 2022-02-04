# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter
from pydantic import UUID4

from app.celery.schemas import AsyncTaskStatus
from app.celery.async_celery import async_result, task_result


router = APIRouter()


@router.get("/{taskId}", response_model = AsyncTaskStatus)
async def get_status(taskId: UUID4) -> dict:
    """ Retrieve asynchronous task result """
    
    async_result_task = await async_result(taskId)
    print (type(async_result_task.result))
    return {
        "taskId": taskId, 
        "taskStatus": async_result_task.status}

@router.get("/{taskId}/result/")
async def get_task_result(taskId: UUID4) -> Any:
    """ Retrieve asynchronous task result """
    
    return await task_result(await async_result(taskId))