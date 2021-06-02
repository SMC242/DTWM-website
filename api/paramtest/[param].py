from sanic import Sanic
from sanic.response import json, HTTPResponse
from sanic.request import Request
app = Sanic(name="DTWM API parameters test")


@app.route("/api/paramtest/<test:string>")
async def pathtest(request: Request, param="failed") -> HTTPResponse:
    return json({"Parameter works": param})
