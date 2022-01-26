# -*- coding: utf-8 -*-

from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger

from app.core.config import settings


logger = get_task_logger(__name__)

app = Celery(name='worker', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND_URL)
app.conf.update(
    redis_socket_keepalive=True, # Keep healthy connection with redis
    #task_serializer = 'pickle',
    #result_serializer = 'pickle',
    accept_content = ['application/json', 'application/x-python-serialize']
) 


@app.task(
    name="sleep", 
    bind=True, # Give us access to task instance through self
    worker_prefetch_multiplier=1, # prefetching is not disable, but reduce to the minimum
    max_retries=settings.CELERY_MAX_RETRIES, 
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT, 
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT)
def upload_csv_data(self, time:int):
    """ celery task - sleep some time """
    
    try:
        sleep(time)
        return  {"message": f"I'm well sleeping {time} seconds"}
    
    except Exception as exc:
        logger.error(f"Exception in celery task !")
        logger.exception(exc)
        self.retry(exc=exc)