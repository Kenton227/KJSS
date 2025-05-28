from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src import database as db
import sqlalchemy
from typing import List
from src.db.schemas import GameModel, Color

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{game_id}", response_model=GameModel)
def get_game(game_id: int):
    # retrieves black and white player id given a game id
    with db.engine.begin() as connection:
        game_data = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    black,
                    white,
                    winner,
                    time_control,
                    duration_in_ms,
                    date_played
                FROM games
                WHERE id = :game_id
                """
            ),
            [
                {
                    "game_id": game_id,
                }
            ],
        ).one_or_none()
        if game_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"No game found with id: {game_id}"
            )

    return GameModel(
        black=game_data.black,
        white=game_data.white,
        winner=Color[game_data.winner] if game_data.winner != "draw" else None,
        time_control=game_data.time_control,
        duration_in_ms=game_data.duration_in_ms,
        date_played=game_data.date_played.date()
    )

@router.get("/games/search", response_model=List[GameModel])
def search_games(player_query:str="", time_control_query:str=""):
    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    black,
                    white,
                    winner,
                    time_control,
                    duration_in_ms,
                    date_played
                FROM games as g
                JOIN users as bp on bp.id = g.black
                JOIN users as wp on wp.id = g.white
                WHERE
                    (bp.username ILIKE '%' || :player_query ||'%'
                        OR wp.username ILIKE '%' || :player_query ||'%')
                    AND (time_control ILIKE '%' || :time_query ||'%')
                ORDER BY date_played DESC
                """
            ),
            [{ "player_query": player_query, "time_query": time_control_query }]
        ).all()
    
    return [
        GameModel(
            black=row.black,
            white=row.white,
            winner=Color[row.winner] if row.winner != "draw" else None,
            time_control=row.time_control,
            duration_in_ms=row.duration_in_ms,
            date_played=row.date_played.date()
        )
        for row in results
    ]