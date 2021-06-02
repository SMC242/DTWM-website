from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }
