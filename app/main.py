import os
from fastapi import FastAPI
from routers.smiles import router as smiles_router
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(smiles_router, prefix="/smiles", tags=["Smiles"])


@app.get("/")
async def get_server():
    return {"server_id": os.getenv("SERVER_ID", "1")}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
