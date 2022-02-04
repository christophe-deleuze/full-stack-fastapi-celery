# -*- coding: utf-8 -*-

from typing import Any
from asyncio import sleep

from celery import Celery
from pydantic import UUID4
from fastapi import HTTPException
from celery.result import AsyncResult
from asgiref.sync import sync_to_async

from app.core.config import settings


app = Celery(name='tasks-producer', 
             broker=settings.CELERY_BROKER_URL, 
             backend=settings.CELERY_RESULT_BACKEND_URL)

app.conf.update(
    broker_transport_options = {
        "confirm_publish": True, 
        "max_retries": 5 }, 
    redis_socket_keepalive=True, 
    accept_content = ['application/json', 'application/x-python-serialize']
)

async def send_task(
    *args, 
    **kwargs
    ) -> AsyncResult:
    """ Send a task with overwriting retry and retry_policy and return an AsyncResult """
    
    # Send task to rabbitMq and return async_result
    return await sync_to_async(app.send_task)(
        *args, 
        **kwargs, 
        retry = settings.CELERY_SEND_TASK_RETRY, 
        retry_policy = settings.CELERY_SEND_TASK_RETRY_POLICY) 

async def async_result(task_id: UUID4) -> AsyncResult:
    """ Get an AsyncResult from a task_id """
    
    return await sync_to_async(app.AsyncResult)(str(task_id))

async def task_result(
    async_result: AsyncResult, 
    celery_request_time_out: int = settings.CELERY_REQUEST_TIME_OUT
    ) -> Any:
    """ Get a task result from an AsyncResult """
    
    timelapse = 0.0
    delay = 0.1
    while not async_result.ready() and (timelapse < settings.CELERY_REQUEST_TIME_OUT) :
        await sleep(delay)
        delay = min(delay * 1.5, 2) # exponential backoff, max 2 seconds
        timelapse += delay
    
    if timelapse > settings.CELERY_REQUEST_TIME_OUT :
        # Generate error message before revoke
        detail = f"FastAPI Request Timeout - Celery task '{async_result.task_id}' with state '{async_result.state}' should be revoke"
        # Any worker receiving the task, or having reserved the task, must ignore it.
        async_result.revoke()
        raise HTTPException(status_code=408, detail=detail)
    
    if async_result.failed():
        detail = f"Celery task '{async_result.task_id}' failed with the following traceback:\n {async_result.traceback}"
        # forget result and raise HTTPException
        async_result.forget()
        raise HTTPException(status_code=500, detail=detail)
    
    # Wait the result into redis backend
    result = await sync_to_async(async_result.get)(celery_request_time_out-timelapse)
    
    # Once the result is retrieved, forget the task inside redis backend to free memory
    async_result.forget()
    
    return result
