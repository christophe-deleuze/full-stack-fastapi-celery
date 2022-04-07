# -*- coding: utf-8 -*-

from pydantic import BaseModel, UUID4


class AsyncTask(BaseModel):
    taskId: UUID4


class AsyncTaskStatus(BaseModel):
    taskId: UUID4
    taskStatus: str
