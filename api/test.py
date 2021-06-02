from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def test_standalone_app() -> dict:
    return {"message": "Standalone app works"}
