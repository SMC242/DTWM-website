from sanic import Sanic
from sanic.response import json, HTTPResponse
from sanic.request import Request
app = Sanic(name="DTWM API root")


@app.route('/')
async def index(request: Request):
    return json({'hello': "yes"})
