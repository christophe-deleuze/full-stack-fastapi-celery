# -*- coding: utf-8 -*-

from functools import wraps

from FastAPI import HTTPException
from celery.result import AsyncResult

from app.core.config import settings
from app.core.celery.async_celery import send_task
from app.core.celery.responses import task_sync_response, task_async_response


def send_task_and_handle_async_result_synchronously(
    task_name: str, 
    task_queue: str, 
    task_serializer: str = settings.CELERY_STANDARD_SERIALIZER, 
    celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT, 
    celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT):
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """ Send task and wait until task is ready then return the result though a standard celery sync response """
            
            # Retrieve Celery AsyncResult
            async_result = await send_task(
                task_name,
                args = tuple(*args),
                kwargs= dict(**kwargs),
                serializer = task_serializer,
                queue = task_queue)
            
            # Await until task is ready then return the result
            result = await task_sync_response(
                async_result,
                celery_task_ready_time_out = celery_task_ready_time_out,
                celery_task_result_time_out = celery_task_result_time_out)
            
            return result
        return wrapper

def send_task_and_handle_async_result_asynchronously(
    task_name: str, 
    task_queue: str, 
    task_serializer: str = settings.CELERY_STANDARD_SERIALIZER):
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
           """ Send task and return standard celery async response """
            
            # Retrieve Celery AsyncResult
            async_result = await send_task(*args, **kwargs)
            
            # Return  Celery AsyncResult id
            return await task_async_response(async_result)
        return wrapper

def handle_async_result_synchronously( 
    celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT, 
    celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT):
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """ Wait until task is ready then return the result though a standard celery sync response """
            
            # Call function and retrieve potential AsyncResult
            async_result = await func(*args, **kwargs)
            
            # Everything which is not an AsyncResult should be ignore 
            if not isinstance(async_result, AsyncResult):
                raise HTTPException(status_code="409", detail="Handler support only celery AsyncResult!")
            
            # Await until task is ready then return the result
            result = await task_sync_response(
                async_result,
                celery_task_ready_time_out = celery_task_ready_time_out,
                celery_task_result_time_out = celery_task_result_time_out)
            
            return result
        return wrapper

def handle_async_result_asynchronously(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """ Return standard celery async response """
        
        # Everything which is not an AsyncResult should be ignore 
        if not isinstance(async_result, AsyncResult):
            raise HTTPException(status_code="409", detail="Handler support only celery AsyncResult!")
        
        # Return  Celery AsyncResult id
        result = await task_async_response(async_result)
        return result
    return wrapper