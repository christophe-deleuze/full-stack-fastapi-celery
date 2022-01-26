# -*- coding: utf-8 -*-

from fastapi import APIRouter

from app.api.api_v1.endpoints import project_worker, tasks


api_v1 = APIRouter()

api_v1.include_router(project_worker.router, prefix="/project-worker", tags=["project-worker"])
api_v1.include_router(tasks.router, prefix="/tasks", tags=["tasks"])