from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
import sqlalchemy
from src import database as db

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
    if game_id not in db:
        return {"detail": f"Game with ID {game_id} not found"}
    game_data = db[game_id]
    return Game(id=game_id, **game_data)
