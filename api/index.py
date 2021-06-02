from sanic import Sanic
from sanic.response import json, HTTPResponse
from sanic.request import Request
app = Sanic(name="DTWM API root")


@app.route('/')
@app.route('/<path:path>')
async def index(request: Request, path=""):
    return json({'hello': path})
