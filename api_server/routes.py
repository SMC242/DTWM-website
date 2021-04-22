from fastapi import HTTPException, APIRouter, Body
from fastapi.encoders import jsonable_encoder
from functions.teamkill_leaderboard import main, outfit_id_by_tag, TKTable
from models import TKBoard
router = APIRouter()


def tk_board_not_found(tag: str):
    """Create an error response for if an outfit tag doesn't exist."""
    raise HTTPException(404, f"Could not find {tag}")


def tk_board_nso_error(tag: str):
    raise HTTPException(
        400, f"{tag} appears to be an NSO outfit. Getting their TKs is not supported")


def tk_board_response(outfit_tag: str) -> TKBoard:
    """Build the response for a successful teamkill board query."""
    def tk_board_response_inner(tk_board: TKTable) -> dict:
        number_of_chars = len(tk_board)
        return {
            "outfit_tag": outfit_tag,
            "number_of_chars": number_of_chars,
            "board": tk_board
        }
    return tk_board_response_inner


@router.get("/teamkill-board/{outfit_tag}", response_model=TKBoard)
async def get_tk_board(outfit_tag: str) -> dict:
    """Get the teamkill leadboard for the given outfit ID"""
    id = await outfit_id_by_tag(outfit_tag)
    if not id:
        tk_board_not_found(outfit_tag)

    try:
        board = await main(id)
        return tk_board_response(outfit_tag)(board)
    except ValueError:
        tk_board_nso_error(outfit_tag)
