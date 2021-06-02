from sanic import Sanic
from sanic.response import json, Request, HTTPResponse
app = Sanic(name="DTWM API root")


@app.route('/')
@app.route('/<path:path>')
async def index(request: Request, path=""):
    return json({'hello': path})


@app.route("/pathtest")
async def pathtest(request) -> HTTPResponse:
    return json({"non-index path works"})
