# -*- coding: utf-8 -*-

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_NAME: str = "Project API"
    API_VERSION: str = "0.1.0"
    API_V1_PATH: str = "/v1"
    API_DESCRIPTION: str = """ Project API is like a proxy to launch celery tasks and to query PostgreSQL 🚀 

## API Features

- Produce celery tasks ;
- Produce celery worflow ;
- Query PostgreSQL Database ;
- Retrieve celery results synchronously and asynchronously;

### What is usefull with this software architecture ?

- API and workers are separated (The API couldn't be overloaded easily this way) ;
- Celery allow to distribute work by using canvas, which is usefull for heavy process ;
- Celery (through rabbitMQ) is connected to prometheus, which enable to autoscale workers on queue length ;
- Celery is helpful to distribute heavy process or launch background tasks.

### What is paintfull with this software architecture ?

- Celery is not optimized for small job.

### How about the global architecture  ?

The project is separated in 2 parts :
- project-api
- project-worker

#### project-api :

The API is dedicated for input data validation and tasks production.
- Celery is not natively compatible with asyncio, then the common celery functions are wrapped in **app/celery/async_celery.py** to keep the API full async ;
- Mapping celery tasks and fastapi endpoints is done in **/app/api/api_v1/endpoints/project_worker.py** (1 **.py** file for each specific worker project) ;
- 1 celery task = 1 endpoint
- 1 workflow = 1 endpoint

#### project-worker :
The Celery worker project is dedicated to process tasks.
- Each celery-worker manage its own distribution and concurrency ;
- The queue consumed by a celery worker has to be the same as the endpoints queue (use to produce tasks) ; 
- Isolate queue = Isolate project ;
- You could use prometheus and rabbitMQ metrics exporter to manage auto-scaling on queue length.
"""
    
    # Postgres common parameters
    POSTGRES_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1/postgres"
    
    # FastAPI timeout for every Celery task
    CELERY_REQUEST_TIME_OUT: int = 360
    
    # Celery parameters
    CELERY_BROKER_URL: str = 'pyamqp://guest:guest@127.0.0.1:5672//'
    CELERY_RESULT_BACKEND_URL: str = 'redis://127.0.0.1:6379/0'
    CELERY_SEND_TASK_RETRY: bool = True
    CELERY_SEND_TASK_RETRY_POLICY: dict = {"max_retries":3, "interval_start":3, "interval_step":1, "interval_max":6}
    
    # project-worker config
    PROJECT_WORKER_QUEUE = "project-worker"

settings = Settings()