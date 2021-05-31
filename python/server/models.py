from pydantic import BaseModel
from typing import List


class TKRecord(BaseModel):
    name: str
    tks: int


class TKBoard(BaseModel):
    """The schema for a teamkill-leaderboard response."""
    number_of_chars: int
    board: List[TKRecord]
    outfit_tag: str
