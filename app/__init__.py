import os
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.init_db import setup_initial_data
from app.routers.smiles import router as smiles_router
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    setup_initial_data()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(smiles_router, prefix="/smiles", tags=["Smiles"])


@app.get("/")
async def get_server():
    return {"server_id": os.getenv("SERVER_ID", "1")}
