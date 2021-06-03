from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, JSON
from sanic.exceptions import SanicException


from sanic_openapi import openapi3_blueprint
from sanic_limiter import Limiter, get_remote_address

from .._functions.teamkill_leaderboard import outfit_id_by_tag, main


app = Sanic("DTWM API teamkill leadboard endpoint")
app.blueprint(openapi3_blueprint)
limiter = Limiter(app, key_func=get_remote_address)


def tag_not_found_error(tag: str) -> str:
    raise SanicException(f"Tag ('{tag}') not found.", status_code=404)


def nso_outfit_error(tag: str) -> str:
    raise SanicException(
        f"'{tag}' is an NSO outfit. NSO are not supported.", status_code=422)


@app.route("/api/teamkill-board/<outfit_tag:string>")
@limiter.limit("10/hour;1/minute")
async def tkboard(request: Request, outfit_tag: str) -> HTTPResponse:
    """Get a leaderboard of teamkills per 250 kills from an outfit tag."""
