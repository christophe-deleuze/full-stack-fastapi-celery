# -*- coding: utf-8 -*-

from celery import group, chain
from celery.result import AsyncResult

from app.project_worker import signature_integer_multiplication, signature_integers_sum


def chain_integer_multiplication(
    integer: int, 
    nb_chains: int) -> AsyncResult:
    """ Launch x tasks in chain """
    
    # Define the initial task with explicit arg
    initial_task = signature_integer_multiplication(integer)
    
    # Define the chain task without arg, because arg should be feed by the previous task
    chain_tasks = (signature_integer_multiplication,)*nb_chains
    
    # Chain all tasks and return AsyncResult
    return chain(initial_task, *chain_tasks)()

def group_integer_multiplication_and_chain_sum(
    integer: int, 
    nb_groups: int) -> AsyncResult:
    """ Launch x parallel tasks then sum all the results """
    
    # Define the signatures of same individuals tasks (Pack in a tuple)
    group_tasks = (signature_integer_multiplication(integer),)*nb_groups
    
    # Define the signature of the final task which should be the sum
    final_task = signature_integers_sum
    
    # Unpack all singles tasks in group, then pass all results to the final task (chain) which return an AsyncResult
    return chain(group(*group_tasks), final_task)()
