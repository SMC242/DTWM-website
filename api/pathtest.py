from sanic import Sanic
from sanic.response import json, HTTPResponse
from sanic.request import Request
app = Sanic(name="DTWM API path testing")


@app.route("/api/pathtest")  # must prefix with /api/
async def pathtest(request: Request) -> HTTPResponse:
    return json({"non-index path works": True})
