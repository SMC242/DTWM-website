from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, JSON

from sanic_openapi import openapi3_blueprint


app = Sanic("DTWM API index endpoint")
app.blueprint(openapi3_blueprint)


@app.route("/")
async def index(request: Request) -> HTTPResponse:
    return JSON({"message": "This is the DTWM API. Please visit /api/swagger if you are a developer. Otherwise, it's best to leave."})
