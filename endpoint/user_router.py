from http import HTTPStatus
from fastapi import APIRouter
from schema.user import User
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
user_service = UserService()


@router.get("/", status_code=HTTPStatus.OK)
async def get_users():
    return user_service.get_users()

@router.post("/", status_code=HTTPStatus.CREATED)
async def add_user(user: User):
    return user_service.create_user(user)

@router.get("/{user_id}", status_code=HTTPStatus.OK)
async def get_user(user_id: int):
    return user_service.get_user(user_id)

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int):
    return user_service.delete_user(user_id)

@router.put("/{user_id}")
async def update_user(user_id: int, req_user: User):
    return user_service.update_user(user_id, req_user)  

@router.patch("/{user_id}/age/increment")
async def increment_age(user_id: int):
    return user_service.increment_age(user_id)

@router.patch("/{user_id}/age/decrement")
async def decrement_age(user_id: int):
    return user_service.decrement_age(user_id)

