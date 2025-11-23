import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import weather

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("[System] DB Initialized.")
    except Exception as e:
        print(f"[System] DB Initialization Failed: {e}")
    yield
    print("[System] App Shutdown.")

app = FastAPI(lifespan=lifespan)

app.include_router(weather.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI Weather Server is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)