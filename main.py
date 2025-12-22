from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


app.include_router(debtor_router)