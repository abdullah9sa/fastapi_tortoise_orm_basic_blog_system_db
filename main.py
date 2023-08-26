# Task 2 - Abdullah Salih

from fastapi import FastAPI
from app.dependencies.database import Tortoise, init_tortoise,close_tortoise
from app.routes import user_routes, post_routes
from fastapi.testclient import TestClient
from tests.user_routes_test import *

app = FastAPI()
client = TestClient(app)

@app.on_event("startup")
async def startup_db():
    await init_tortoise(app)

@app.on_event("shutdown")
async def shutdown_db():
    await close_tortoise(app)


app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(post_routes.router, prefix="/posts", tags=["posts"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


