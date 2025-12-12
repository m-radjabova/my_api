from fastapi import APIRouter

from services.todos_service import Todo, TodosService


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

todos_service = TodosService()

@router.get("/", status_code=200)
async def get_todos():
    return todos_service.get_todos()


@router.post ("/", status_code=201)
async def create_todo(todo: Todo):
    return todos_service.create_todo(todo)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    return todos_service.delete_todo(todo_id)


@router.put("/{todo_id}", status_code=200)
async def update_todo(todo_id: int, todo: Todo):
    return todos_service.update_todo(todo_id, todo)


@router.get("/user/{user_id}", status_code=200)
async def get_todos_by_user_id(user_id: int):
    return todos_service.get_todo_by_user_id(user_id)


@router.patch("/{todo_id}/completed")
def toggle_todo(todo_id: int):
    return todos_service.toogle_todo_completed(todo_id)

