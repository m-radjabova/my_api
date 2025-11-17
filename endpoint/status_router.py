from http import HTTPStatus
from typing import List
from fastapi import APIRouter

from schema.status import Status
from services.status_service import StatusService

router = APIRouter(prefix="/status", tags=["STATUS"])
status_service = StatusService()


@router.get("/types")
async def get_status_types():
    return status_service.get_status_type()


@router.post("/create", response_model=Status)
async def add_status_task(status_type: str):
    return status_service.add_task_status(status_type)


@router.get("/list", response_model=List[Status], status_code=HTTPStatus.OK)
async def get_task_status():
    return status_service.get_status_task()
