from fastapi import APIRouter
from schema.status import StatusType
from schema.task import Task
from services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])
tasks_service = TaskService()


@router.get("/", status_code=200)
async def get_tasks():
    return tasks_service.get_tasks()


@router.post("/", status_code=201)
async def add_task(task: Task):
    return tasks_service.add_task(task)


@router.get("/priority", status_code=200)
async def get_task_priority():
    return tasks_service.get_task_priority()

@router.get("/status/{status}", status_code=200)
async def get_tasks_by_status(status: StatusType):
    return tasks_service.get_tasks_by_status(status)


@router.delete("/{task_id}", status_code=200)
async def delete_task(task_id: int):
    return tasks_service.delete_task(task_id)

@router.put("/{task_id}", status_code=200)
async def update_task(task_id: int, task: Task):
    return tasks_service.update_task(task_id, task)