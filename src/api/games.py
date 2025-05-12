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


@router.get("/{game_id}", response_model=Game)
def get_game(game_id: int):
    # retrieves black and white player id given a game id
    with db.engine.begin() as connection:
        game_data = connection.execute(
            sqlalchemy.text(
                """
                SELECT black, white
                FROM games
                WHERE id = :game_id
                """
            ),
            [
                {
                    "game_id": game_id,
                }
            ],
        ).one()
        black_id = game_data.black
        white_id = game_data.white

    return Game(black_player_id=black_id, white_player_id=white_id)
