import os
from fastapi import FastAPI
from routers.smiles import router as smiles_router

app = FastAPI()
app.include_router(smiles_router, prefix="/smiles", tags=["Smiles"])


@app.get("/")
async def get_server():
    return {"server_id": os.getenv("SERVER_ID", "1")}
