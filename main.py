from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoint.user_router import router as user_router
from endpoint.status_router import router as status_router
from endpoint.task_router import router as task_router

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
app.include_router(status_router)
app.include_router(task_router)
