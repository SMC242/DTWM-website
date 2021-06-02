from fastapi import FastAPI
from uvicorn import run

app = FastAPI()
print("App running")


@app.get("/test")
async def test_standalone_app() -> dict:
    return {"message": "Standalone app works"}

if __name__ == "__main__":
    run(app)
