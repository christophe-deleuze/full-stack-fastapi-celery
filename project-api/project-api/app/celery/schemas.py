# -*- coding: utf-8 -*-

from uuid import UUID

from pydantic import BaseModel


class AsyncTask(BaseModel):
    task_id: UUID

class AsyncTaskStatus(BaseModel):
    task_id: UUID
    task_status: str
    task_result: bool