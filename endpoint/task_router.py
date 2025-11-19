from fastapi import APIRouter, HTTPException
from typing import List
from schema.task import RequestTask, ResponseTask, Task
from services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])
tasks_service = TaskService()


@router.get("/task-status", status_code=200)
async def get_tasks_status():
    return tasks_service.get_task_status()


@router.get("/", response_model=List[ResponseTask])
async def get_tasks():
    return tasks_service.get_tasks()


@router.post("/", response_model=Task, status_code=201)
async def create_task(task: RequestTask):
    return tasks_service.create_task(task)


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: RequestTask):
    updated = tasks_service.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    deleted = tasks_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
