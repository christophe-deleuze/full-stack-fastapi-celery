# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter


router = APIRouter()


#@router.post("/integer-multiplication/")
#async def post_integer_multiplication(
#    integer : int
#    ) -> Any:
#    """ Call directly project-worker task : integer-multiplication """
#    
#    return await send_task_and_wait_result(
#        "integer-multiplication", 
#        args = (integer,), 
#        serializer = "json", 
#        queue = settings.PROJECT_WORKER_QUEUE)
#
#@router.post("/integer-multiplication/async/")
#async def post_integer_multiplication_async(
#    integer : int
#    ) -> Any:
#    """ Call directly project-worker task : integer-multiplication and retrieve task id to get the result later """
#    
#    return await send_task(
#        "integer-multiplication", 
#        args = (time,), 
#        serializer = "json", 
#        queue = settings.PROJECT_WORKER_QUEUE)