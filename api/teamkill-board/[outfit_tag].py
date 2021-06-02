from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, JSON

from sanic_openapi import openapi3_blueprint

from .._functions.teamkill_leaderboard import outfit_id_by_tag, main


app = Sanic("DTWM API teamkill leadboard endpoint")
app.blueprint(openapi3_blueprint)


def tag_not_found_error(tag: str) -> str:
    

@app.route("/api/teamkill-board/<outfit_tag:string>")
async def tkboard(request: Request, outfit_tag: str) -> HTTPResponse:
    """Get a leaderboard of teamkills per 250 kills from an outfit tag."""
