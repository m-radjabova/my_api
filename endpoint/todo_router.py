from http import HTTPStatus
from fastapi import APIRouter

from schema.todo import Todo
from services.todo_service import TodoService

todo_service = TodoService()

router = APIRouter(
    prefix="/todos",
    tags=["todo"],
)

@router.get("/", status_code=HTTPStatus.OK)
async def get_todos():
    return todo_service.get_todos()

@router.post("/", status_code=HTTPStatus.CREATED)
async def add_todo(todo: Todo):
    return todo_service.add_todo(todo)

@router.get("/{todo_id}", status_code=HTTPStatus.OK)
async def get_todo(todo_id: int):
    return todo_service.get_todo(todo_id)

@router.delete("/{todo_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_todo(todo_id: int):
    return todo_service.delete_todo(todo_id)

@router.put("/{todo_id}", status_code=HTTPStatus.OK)
async def update_todo(todo_id: int, req_todo: Todo):
    return todo_service.update_todo(todo_id, req_todo)

@router.patch("/{todo_id}/toggle", status_code=HTTPStatus.OK)
async def toggle_todo(todo_id: int):
    return todo_service.toggle_todo(todo_id)

@router.get("/{user_id}", status_code=HTTPStatus.OK)
async def get_todos_by_userId(user_id: int):
    return todo_service.get_todos_by_userId(user_id)