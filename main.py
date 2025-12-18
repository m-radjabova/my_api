from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from endpoint.users_router import router as users_router
# from endpoint.posts_router import router as posts_router
# from endpoint.comment_router import router as comment_router
# from endpoint.todos_router import router as todos_router
# from endpoint.cars_router import router as car_router

from endpoint.debtor_router import router as debtor_router

# uvicorn main:app --reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# app.include_router(users_router)
# app.include_router(posts_router)
# app.include_router(comment_router)
# app.include_router(todos_router)
# app.include_router(car_router)

app.include_router(debtor_router)