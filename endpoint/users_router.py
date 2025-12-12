from fastapi import APIRouter
from services.users_service import User, UsersService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

users_service = UsersService()


@router.get("/", status_code=200)
async def get_users():
    return users_service.get_users()


@router.post("/", status_code=201)
async def add_user(user: User):
    return users_service.create_user(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    return users_service.delete_user(user_id)

@router.put("/{user_id}", status_code=200)
async def update_user(user_id: int, user: User):
    return users_service.update_user(user_id, user)
