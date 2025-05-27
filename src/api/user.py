from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status, Query, HTTPException
import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Self, Optional

from datetime import date
from psycopg import errors
from enum import Enum

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

class Color(str, Enum):
    black = "black"
    white = "white"

class TimeControl(str, Enum):
    classical = "classical"
    rapid = "rapid"
    blitz = "blitz"
    bullet = "bullet"

class GameStatus(str, Enum):
    win = "win"
    loss = "loss"
    draw = "draw"

class GameSubmitData(BaseModel):
    color: Color
    game_status: GameStatus
    time_control: TimeControl
    opponent_id: int
    time_in_ms: int = Field(ge=0, description="Time must be non-zero and non-negative")
    date_played: date


class GameModel(BaseModel):
    black: int
    white: int
    winner: Color | None
    time_control: TimeControl
    duration_in_ms: int = Field(
        ge=0, description="Time must be non-zero and non-negative"
    )
    date_played: date

    @model_validator(mode="after")
    def validate_color(self) -> Self:
        if self.black == self.white:
            raise ValueError("the same player can't be both black and white'")
        return self


class Showcase(BaseModel):
    created_by: int
    title: str
    views: int
    caption: str
    date_created: date
    game_id: int


# TODO: WRITE TEST
def create_game_model(user_id: int, game_data: GameSubmitData) -> GameModel:

    if game_data.color == "white":
        black_player, white_player = game_data.opponent_id, user_id
        winner = "white" if game_data.game_status == "win" else "black"
    else:
        black_player, white_player = user_id, game_data.opponent_id
        winner = "black" if game_data.game_status == "win" else "white"
    
    if game_data.game_status == "draw":
        winner = None

    return GameModel(
        black=black_player,
        white=white_player,
        winner=winner,
        time_control=game_data.time_control,
        duration_in_ms=game_data.time_in_ms,
        date_played=game_data.date_played
    )


@router.post("/games/{user_id}/submit", status_code=status.HTTP_204_NO_CONTENT)
def submit_game(user_id: int, submission_data: GameSubmitData):
    game_data = create_game_model(user_id, submission_data)
    print(f"Adding game data: {game_data}")

    with db.engine.begin() as connection:
        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO games (black, white, winner, time_control, duration_in_ms, date_played)
                    VALUES
                        (
                            :black_player_id,
                            :white_player_id,
                            :winner,
                            :time_control,
                            :time,
                            :date
                        )
                    ON CONFLICT DO NOTHING
                    RETURNING id
                    """
                ),
                [
                    {
                        "black_player_id": game_data.black,
                        "white_player_id": game_data.white,
                        "winner": game_data.winner if game_data.winner else "draw",
                        "time_control": game_data.time_control,
                        "time": game_data.duration_in_ms,
                        "date": game_data.date_played
                    }
                ],
            )
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                raise HTTPException(
                    status_code=422,
                    detail=f"Bad player IDs"
                )



@router.get("/games/{user_id}", response_model=List[GameModel])
def get_history(user_id: int) -> List[GameModel]:
    with db.engine.begin() as connection:
        result = connection.execute(
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
                WHERE black = :user_id OR white = :user_id
                ORDER BY date_played DESC
                LIMIT 20
                """
            ),
            [{"user_id": user_id}],
        ).all()

        if not result:
            user_confirm = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT id
                    FROM users
                    WHERE id = :user_id
                    """
                ),
                [{"user_id": user_id}]
            ).one_or_none()

            if not user_confirm:
                raise HTTPException(
                    status_code=404,
                    detail=f"User does not exist"
                )
            raise HTTPException(
                status_code=404,
                detail=f"User has not recorded any games"
            )
    
    return [
        GameModel(
            black=row.black,
            white=row.white,
            winner=row.winner,
            time_control=row.time_control,
            duration_in_ms=row.duration_in_ms,
            date_played=row.date_played
        )
        for row in result
    ]


@router.get("/showcases/{user_id}", response_model=List[Showcase])
def get_user_showcases(user_id: int) -> List[Showcase]:
    with db.engine.begin() as connection:
        showcases = connection.execute(
            sqlalchemy.text(
                """
                SELECT created_by, title, views, caption, date_created, game_id
                FROM showcases
                WHERE created_by = :user_id
                ORDER BY date_created DESC
                """
            ),
            {"user_id": user_id},
        ).all()
    return showcases

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register_user(username: str, user_email: Optional[str] = Query(default=None)):
    with db.engine.begin() as connection:
        try: 
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO users(username, email, register_date)
                    VALUES
                        (:username, LOWER(:user_email), DEFAULT)
                    """
                ),
                {
                    "username": username,
                    "user_email": user_email
                }
            )
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                print("TESt")
                raise HTTPException(
                    status_code=422,
                    detail="User or email already in use"
                )
                

