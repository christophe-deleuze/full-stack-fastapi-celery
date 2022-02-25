# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_prometheus import metrics, PrometheusMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_v1


app = FastAPI(
    title=settings.API_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Set all CORS enabled origins
if settings.CORS_ALLOW_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ALLOW_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Collect and expose metrics
app.add_middleware(PrometheusMiddleware) 
app.add_route("/metrics", metrics)

app.include_router(api_v1, prefix=settings.API_V1_PATH)