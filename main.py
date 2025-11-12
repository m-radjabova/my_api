from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoint.user_router import router as user_router
from endpoint.post_router import router as post_router
from endpoint.todo_router import router as todo_router
from endpoint.comment_router import router as comment_router

# uvicorn main:app --reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(todo_router)
app.include_router(comment_router)