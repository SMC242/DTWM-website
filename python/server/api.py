from fastapi import FastAPI
try:
    from server.routes import router
except ImportError:
    from python.server.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }
