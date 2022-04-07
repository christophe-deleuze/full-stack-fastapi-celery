# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.api_v1.endpoints import celery_worker, celery_workflows, tasks

api_v1 = APIRouter()

api_v1.include_router(celery_worker.router, prefix="/celery-worker", tags=["celery-worker"])
api_v1.include_router(celery_workflows.router, prefix="/celery-workflows", tags=["celery-workflows"])
api_v1.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
