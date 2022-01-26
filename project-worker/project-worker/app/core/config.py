# -*- coding: utf-8 -*-

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Celery parameters
    CELERY_BROKER_URL: str = 'pyamqp://guest:guest@127.0.0.1:5672//'
    CELERY_RESULT_BACKEND_URL: str = 'redis://127.0.0.1:6379/0'
    
    CELERY_MAX_RETRIES:int = 5
    CELERY_TASK_TIME_LIMIT:int = 300
    CELERY_TASK_SOFT_TIME_LIMIT:int = 275

settings = Settings()