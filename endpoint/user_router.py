from http import HTTPStatus
from typing import Annotated, List
from fastapi import APIRouter, Query
from schema.user import RequestTeam, RequestUser, User
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

user_service = UserService()

@router.get("/", status_code=HTTPStatus.OK)
async def get_users():
    return user_service.get_users()

@router.post("/",status_code=HTTPStatus.CREATED)
async def add_user(user: RequestUser):
    return user_service.create_user(user)

@router.get("/{user_id}", status_code=HTTPStatus.OK)
async def get_user(user_id: int):
    return user_service.get_user(user_id)

@router.put("/{user_id}", status_code=HTTPStatus.OK)
async def update_user(user_id: int, user: User):
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int):
    user_service.delete_user(user_id)
    return HTTPStatus.NO_CONTENT

