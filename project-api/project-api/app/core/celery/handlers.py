# -*- coding: utf-8 -*-

from typing import Any, Callable
from functools import wraps

from FastAPI import HTTPException
from celery.result import AsyncResult

from app.core.config import settings
from app.core.celery.schemas import AsyncTask
from app.core.celery.async_celery import send_task
from app.core.celery.responses import task_sync_response, task_async_response


def send_task_and_handle_async_result_synchronously(
        task_name: str,
        task_queue: str,
        task_serializer: str = settings.CELERY_STANDARD_SERIALIZER,
        celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT,
        celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            """ Send task and wait until task is ready then return the result though a standard celery sync response """

            # Retrieve Celery AsyncResult
            async_result = await send_task(
                task_name,
                args=tuple(*args),
                kwargs=dict(**kwargs),
                serializer=task_serializer,
                queue=task_queue)

            # Wait until task is ready then return the result
            result = await task_sync_response(
                async_result,
                celery_task_ready_time_out=celery_task_ready_time_out,
                celery_task_result_time_out=celery_task_result_time_out)

            return result

        return wrapper

    return decorator


def send_task_and_handle_async_result_asynchronously(
        task_name: str,
        task_queue: str,
        task_serializer: str = settings.CELERY_STANDARD_SERIALIZER
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> dict[str, str]:
            """ Send task and return standard celery async response """

            # Retrieve Celery AsyncResult
            async_result = await send_task(
                task_name,
                args=tuple(*args),
                kwargs=dict(**kwargs),
                serializer=task_serializer,
                queue=task_queue)

            # Return  Celery AsyncResult id
            return await task_async_response(async_result)

        return wrapper

    return decorator


def handle_async_result_synchronously(
        celery_task_ready_time_out: float = settings.CELERY_TASK_READY_TIME_OUT,
        celery_task_result_time_out: float = settings.CELERY_TASK_RESULT_TIME_OUT
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            """ Wait until task is ready then return the result though a standard celery sync response """

            # Call function and retrieve potential AsyncResult
            async_result = await func(*args, **kwargs)

            # Everything which is not an AsyncResult should be ignored
            if not isinstance(async_result, AsyncResult):
                raise HTTPException(status_code="409", detail="Handler support only celery AsyncResult!")

            # Wait until task is ready then return the result
            result = await task_sync_response(
                async_result,
                celery_task_ready_time_out=celery_task_ready_time_out,
                celery_task_result_time_out=celery_task_result_time_out)

            return result

        return wrapper

    return decorator


def handle_async_result_asynchronously(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> dict[str, str]:
        """ Return standard celery async response """

        async_result = await func(*args, **kwargs)

        # Everything which is not an AsyncResult should be ignored
        if not isinstance(async_result, AsyncResult):
            raise HTTPException(status_code="409", detail="Handler support only celery AsyncResult!")

        # Return  Celery AsyncResult id
        return await task_async_response(async_result)

    return wrapper
