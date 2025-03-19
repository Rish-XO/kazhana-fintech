import os
import uvicorn
from fastapi import FastAPI
from database import engine
from models import Base
from routes import router

app = FastAPI()

# Initialize database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Set default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
