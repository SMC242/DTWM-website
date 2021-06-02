from sanic import Sanic
from sanic.response import json, Request, HTTPResponse
app = Sanic(name="DTWM API parameters test")


@app.route("/paramtest/<param>")
async def pathtest(request: Request, param: str) -> HTTPResponse:
    return json({"Parameter works": param})
