from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager
from pymongo import MongoClient
from src import routes


async def connect_to_database():
    db = MongoClient("mongodb://root:password@mongodb:27017/")
    return db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_host = await connect_to_database()
    app.users = db_host.scheduler.users
    print("startup has begun!")
    yield
    print("shutdown hs begun!")

app = FastAPI(lifespan=lifespan)

app.include_router(routes.auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "https://harsh-diann-task-master-07d5d1e3.koyeb.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
