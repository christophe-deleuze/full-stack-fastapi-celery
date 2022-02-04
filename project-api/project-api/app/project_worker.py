# -*- coding: utf-8 -*-

from typing import Any, List

from celery import signature

from app.core.config import settings
from app.celery.async_celery import task_result, send_task


async def send_task_integer_multiplication(
    integer: int
    ) -> Any:
    """ Send task : integer-multiplication, to project-worker """
    
    return await send_task(
        "integer-multiplication", 
        args = (integer,), 
        serializer = "json", 
        queue = settings.PROJECT_WORKER_QUEUE)

async def send_task_integers_sum(
    integers: List[int] 
    ) -> Any:
    """ Send task : integers-sum, to project-worker """
    
    return await send_task(
        "integers-sum", 
        args = (integers,), 
        serializer = "json", 
        queue = settings.PROJECT_WORKER_QUEUE)


def signature_integer_multiplication(integer: int):
    """ Signature definition of integer-multiplication task for workflow """
    
    s = signature(
        "integer-multiplication", 
        args = (integer,), 
        serializer = "json")
    return s.set(queue=settings.SATELLITE_DATA_QUEUE)

def signature_integers_sum(integers: int):
    """ Signature definition of integers-sum task for workflow """
    
    s = signature(
        "integers-sum", 
        args = (integers,), 
        serializer = "json")
    return s.set(queue=settings.SATELLITE_DATA_QUEUE)