# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_v1


app = FastAPI(
    title=settings.API_NAME, 
    description=settings.API_DESCRIPTION, 
    version=settings.API_VERSION
)

app.include_router(api_v1, prefix=settings.API_V1_PATH)
app.add_middleware(PrometheusMiddleware) # Collect metrics
app.add_route("/metrics", metrics) # Expose metrics