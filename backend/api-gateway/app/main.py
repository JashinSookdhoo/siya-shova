from fastapi import FastAPI
from db.connection import connect_to_db, disconnect_from_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db()

@app.get("/health")
async def health():
    return {"status": "ok"}