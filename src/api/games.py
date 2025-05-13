from pydantic import BaseModel
from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(auth.get_api_key)],
)


class Game(BaseModel):
    black_player_id: int
    white_player_id: int


@router.post("/{game_id}", response_model=Game)
def get_game(game_id: int):
    # TODO: function gets game data given a game id
    pass
