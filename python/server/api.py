from fastapi import FastAPI
from server.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }
