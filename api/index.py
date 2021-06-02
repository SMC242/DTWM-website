from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }


@app.get("/test")
async def test_standalone_app() -> dict:
    return {"message": "Standalone app works"}
