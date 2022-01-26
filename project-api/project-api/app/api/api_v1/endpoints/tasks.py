# -*- coding: utf-8 -*-

from uuid import UUID
from typing import Any

from fastapi import APIRouter

from app.celery.schemas import AsyncTaskStatus
from app.celery.async_celery import async_result, task_result


router = APIRouter()


@router.get("/{task_id}", response_model = AsyncTaskStatus)
async def get_status(task_id: UUID) -> dict:
    """ Retrieve asynchronous task result """
    
    async_result_task = await async_result(task_id)
    return {
        "task_id": task_id, 
        "task_status": async_result_task.status, 
        "task_result": async_result_task.result}

@router.get("/{task_id}/result/")
async def get_task_result(task_id: UUID) -> Any:
    """ Retrieve asynchronous task result """
    
    return await task_result(await async_result(task_id))