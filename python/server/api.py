from fastapi import FastAPI
from routes import router

app = FastAPI()
app.include_router(router)


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }
