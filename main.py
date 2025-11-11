from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schema.post import Post
from schema.user import User
from services.post_service import PostService
from services.todo_service import TodoService
from services.user_service import UserService

# uvicorn main:app --reload

app = FastAPI()

user_service = UserService()
post_service = PostService()
todo_service = TodoService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/users")
async def get_users():
    return user_service.get_users()

@app.post("/users")
async def add_user(user: User):
    return user_service.create_user(user)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return user_service.get_user(user_id)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return user_service.delete_user(user_id)

@app.put("/users/{user_id}")
async def update_user(user_id: int, req_user: User):
    return user_service.update_user(user_id, req_user)  

@app.patch("/users/{user_id}/age/increment")
async def increment_age(user_id: int):
    return user_service.increment_age(user_id)

@app.patch("/users/{user_id}/age/decrement")
async def decrement_age(user_id: int):
    return user_service.decrement_age(user_id)


# posts 

@app.get("/posts")
async def get_posts():
    return post_service.get_posts()

@app.post("/posts")
async def add_post(post: Post):
    return post_service.add_post(post)

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return post_service.get_post(post_id)

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    return post_service.delete_post(post_id)

@app.put("/posts/{post_id}")
async def update_post(post_id: int, req_post: Post):
    return post_service.update_post(post_id, req_post)

# todos

@app.get("/todos")
async def get_todos():
    return todo_service.get_todos()

@app.post("/todos")
async def add_todo(todo: Post):
    return todo_service.add_todo(todo)

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    return todo_service.get_todo(todo_id)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    return todo_service.delete_todo(todo_id)

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, req_todo: Post):
    return todo_service.update_todo(todo_id, req_todo)

@app.patch("/todos/{todo_id}/toggle")
async def toggle_todo(todo_id: int):
    return todo_service.toggle_todo(todo_id)