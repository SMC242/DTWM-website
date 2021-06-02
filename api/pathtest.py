from sanic import Sanic
from sanic.response import json, Request, HTTPResponse
app = Sanic(name="DTWM API path testing")


@app.route("/pathtest")
async def pathtest(request: Request) -> HTTPResponse:
    return json({"non-index path works": True})
