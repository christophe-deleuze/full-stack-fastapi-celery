# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter, Query
from pydantic import UUID4

from app.core.celery.schemas import AsyncTaskStatus
from app.core.celery.async_celery import task_async_result, task_result


router = APIRouter()


@router.get("/{taskId}", response_model = AsyncTaskStatus)
async def get_status(
    taskId: UUID4 = Query(None, description="Task UUID4")
    ) -> dict:
    """ Retrieve asynchronous task result """
    
    async_result = await task_async_result(taskId)
    return {
        "taskId": taskId, 
        "taskStatus": async_result.status}

@router.get("/{taskId}/result/")
async def get_task_result(
    taskId: UUID4 = Query(None, description="Task UUID4"),
    forgetRetrievedResult: bool = Query(True, description="Forget task result in the backend once retrieved.")
    ) -> Any:
    """ Retrieve asynchronous task result """
    
    async_result = await task_async_result(taskId)
    return await task_result(async_result, forget_retrieved_result=forgetRetrievedResult)