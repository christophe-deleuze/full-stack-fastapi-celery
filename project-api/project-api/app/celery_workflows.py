# -*- coding: utf-8 -*-

from celery.result import AsyncResult
from celery import group, chain, signature, chord

from app.core.config import settings


async def chain_integers_multiplication(
        integer: int,
        nb_chains: int
) -> AsyncResult:
    """ Launch x tasks in chain """

    # Define the initial task with explicit arg
    initial_task = signature(
        "integer-multiplication",
        args=(integer,),
        serializer="json").set(queue=settings.PROJECT_WORKER_QUEUE)

    # Define the chain task without arg, because arg should be feed by the previous task
    chain_tasks = (signature(
        "integer-multiplication",
        serializer="json").set(queue=settings.PROJECT_WORKER_QUEUE),) * nb_chains

    # Chain all tasks and return AsyncResult
    return chain(initial_task, *chain_tasks)()


async def group_integers_multiplication(
        integer: int,
        nb_groups: int
) -> AsyncResult:
    """ Launch x parallel tasks then  return list results """

    # Define the signatures of same individuals tasks (Pack in a tuple)
    group_tasks = (signature(
        "integer-multiplication",
        args=(integer,),
        serializer="json").set(queue=settings.PROJECT_WORKER_QUEUE),) * nb_groups

    # Unpack all singles tasks in group, then pass all results to the final task (chain) which return an AsyncResult
    return group(group_tasks)()


async def chord_integers_multiplication(
        integer: int,
        nb_groups: int
) -> AsyncResult:
    """ Launch x parallel tasks then sum all the results """

    # Define the signatures of same individuals tasks (Pack in a tuple)
    group_tasks = (signature(
        "integer-multiplication",
        args=(integer,),
        serializer="json").set(queue=settings.PROJECT_WORKER_QUEUE),) * nb_groups

    # Define the signature of the final task (without args) which should be the sum
    final_task = signature(
        "integers-sum",
        serializer="json").set(queue=settings.PROJECT_WORKER_QUEUE)

    # Unpack all singles tasks in group, then pass all results to the final task (chain) which return an AsyncResult
    return chord(group_tasks, final_task)()
