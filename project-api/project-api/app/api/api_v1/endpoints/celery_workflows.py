# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter, Query

from app.core.celery.schemas import AsyncTask
from app.core.celery.responses import task_sync_response, task_async_response
from app.celery_workflows import chain_integers_multiplication, group_integers_multiplication, chord_integers_multiplication

router = APIRouter()


@router.post("/chain-integers-multiplication/")
async def post_chain_integers_multiplication(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_chains: int = Query(None, description="How many chain multiplication by 2 do you want ?")
    ) -> Any:
    """ Send workflow task : chain-integers-multiplication and wait for the result """
    
    async_result = await chain_integers_multiplication(integer, nb_chains)
    return await task_sync_response(async_result)

@router.post("/chain-integers-multiplication/async/", response_model = AsyncTask)
async def post_chain_integers_multiplication_async(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_chains: int = Query(None, description="How many chain multiplication by 2 do you want ?")
    ) -> Any:
    """ Send workflow task : chain-integers-multiplication and retrieve taskId to get the result later """
    
    async_result = await chain_integers_multiplication(integer, nb_chains)
    return await task_async_response(async_result)

@router.post("/group-integers-multiplication/")
async def post_group_integers_multiplication(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_groups: int = Query(None, description="How many single multiplication by 2 do you want ?")
    ) -> Any:
    """ Send workflow task : group-integers-multiplication and wait for the result """
    
    async_result = await group_integers_multiplication(integer, nb_groups)
    return await task_sync_response(async_result)

@router.post("/group-integers-multiplication/async/", response_model = AsyncTask)
async def post_group_integers_multiplication_async(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_groups: int = Query(None, description="How many single multiplication by 2 do you want ?")
    ) -> Any:
    """ Send workflow task : group-integers-multiplication and retrieve taskId to get the result later """
    
    async_result = await group_integers_multiplication(integer, nb_groups)
    return await task_async_response(async_result)

@router.post("/chord-integers-multiplication/")
async def post_chord_integers_multiplication(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_groups: int = Query(None, description="How many single multiplication by 2 do you want before to sum all of them ?")
    ) -> Any:
    """ Send workflow task : chord-integers-multiplication and wait for the result """
    
    async_result = await chord_integers_multiplication(integer, nb_groups)
    return await task_sync_response(async_result)

@router.post("/chord-integers-multiplication/async/", response_model = AsyncTask)
async def post_chord_integers_multiplication_async(
    integer: int = Query(None, description="Integer to multiply by 2."),
    nb_groups: int = Query(None, description="How many single multiplication by 2 do you want before to sum all of them ?")
    ) -> Any:
    """ Send workflow task : chord-integers-multiplication and retrieve taskId to get the result later """
    
    async_result = await chord_integers_multiplication(integer, nb_groups)
    return await task_async_response(async_result)