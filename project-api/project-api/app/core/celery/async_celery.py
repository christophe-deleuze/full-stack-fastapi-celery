# -*- coding: utf-8 -*-

from typing import Any
from asyncio import sleep

from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from pydantic import UUID4
from fastapi import HTTPException

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

async def task_ready(
    async_result: AsyncResult, 
    revoke_task_on_timeout: bool = True, 
    celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT
    ) -> None:
    """ Get a task result from an AsyncResult """
    
    # exponential backoff on task ready, max 2 seconds
    timelapse = 0.0
    delay = 0.1
    while not async_result.ready() and (timelapse < celery_task_ready_time_out) :
        await sleep(delay)
        delay = min(delay * 1.5, 2)
        timelapse += delay
    
    if timelapse > celery_task_ready_time_out :
        # Generate error message before revoke
        detail = f"Timeout ({celery_task_ready_time_out}s) exceed - Task {async_result.id!r} (state: {async_result.state!r}) is not ready."
        
        # Any worker receiving the task, or having reserved the task, must ignore it.
        if revoke_task_on_timeout :
            detail += " Task should be revoke!"
            async_result.revoke()
        raise HTTPException(status_code=408, detail=detail)

async def task_result(
    async_result: AsyncResult, 
    forget_retrieved_result: bool = True, 
    celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT
    ) -> Any:
    """ Get a task result from an AsyncResult """
    
    if async_result.failed():
        detail = f"Celery task {async_result.id!r} failed with the following traceback:\n {async_result.traceback}."
        
        # forget result and raise HTTPException
        if forget_retrieved_result :
            detail += " Task should be forget!"
            async_result.forget()
        raise HTTPException(status_code=500, detail=detail)
    
    try :
        # Wait the result into redis backend
        result = await sync_to_async(async_result.get)(celery_task_result_time_out)
    except Exception as e:
        # To avoid conflict with FastAPI TimeoutError handling, celery TimeoutError is managed through Exception by using isinstance().
        if isinstance(e, TimeoutError):
            detail = f"Timeout ({celery_task_result_time_out}s) exceed - Task {async_result.id!r} (state: {async_result.state!r}) is not ready or not exist."
            status_code = 408
        else :
            detail = f"Exception occured when trying to retrieve task {async_result.id!r} result (state: {async_result.state!r}) ({celery_task_result_time_out}s). Exception message: {e}"
            status_code = 500
        raise HTTPException(status_code=status_code, detail=detail)
    
    # Once the result is retrieved, forget the task inside redis backend to free memory
    if forget_retrieved_result :
        async_result.forget()
    
    return result

async def task_async_result(task_id: UUID4) -> AsyncResult:
    """ Get an AsyncResult from a task_id """
    
    # NB: UUID4 is used for Typing, but celery required an str
    return await sync_to_async(app.AsyncResult)(str(task_id))