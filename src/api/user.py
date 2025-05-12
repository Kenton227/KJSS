from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Self

from datetime import date

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)


class GameSubmitData(BaseModel):
    color: str
    game_status: str
    time_control: str
    opponent_id: int
    time_in_ms: int = Field(ge=0, description="Time must be non-zero and non-negative")

    @field_validator("color")
    @classmethod
    def validate_color(cls, color: str) -> str:
        if not color in ["black", "white"]:
            raise ValueError("color must either be 'black' or 'white'")
        return color

    @field_validator("game_status")
    @classmethod
    def validate_game_status(cls, game_status: str) -> str:
        if not game_status in ["win", "loss", "draw"]:
            raise ValueError(
                "game status must be one of the following: ['win', 'loss', or 'draw']"
            )
        return game_status

    @field_validator("time_control")
    @classmethod
    def validate_time_control(cls, time_control: str) -> str:
        if not time_control in ["classical", "rapid", "blitz", "bullet"]:
            raise ValueError(
                "time control must be one of the following: ['classical', 'rapid', 'blitz', 'bullet']"
            )
        return time_control


class GameModel(BaseModel):
    black: int
    white: int
    winner: str
    time_control: str
    duration_in_ms: int = Field(
        ge=0, description="Time must be non-zero and non-negative"
    )

    @model_validator(mode="after")
    def validate_color(self) -> Self:
        if self.black == self.white:
            raise ValueError("the same player can't be both black and white'")
        return self

    @field_validator("winner")
    @classmethod
    def validate_game_status(cls, game_status: str) -> str:
        if not game_status in ["black", "white", "draw"]:
            raise ValueError(
                "game status must be one of the following: ['black', 'white', or 'draw']"
            )
        return game_status

    @field_validator("time_control")
    @classmethod
    def validate_time_control(cls, time_control: str) -> str:
        if not time_control in ["classical", "rapid", "blitz", "bullet"]:
            raise ValueError(
                "time control must be one of the following: ['classical', 'rapid', 'blitz', 'bullet']"
            )
        return time_control


class Showcase(BaseModel):
    created_by: int
    title: str
    views: int
    caption: str
    date_created: date
    game_id: int


# TODO: WRITE TEST
def createGameModel(user_id: int, game_data: GameSubmitData) -> GameModel:
    player_colors = []
    BLACK_INDEX = 0
    WHITE_INDEX = 1

    if game_data.color == "white":
        player_colors = [game_data.opponent_id, user_id]
    else:
        player_colors = [user_id, game_data.opponent_id]

    print(f"COLORS: {player_colors[0], player_colors[1]}")
    return GameModel(
        black=player_colors[BLACK_INDEX],
        white=player_colors[WHITE_INDEX],
        winner="black" if player_colors[BLACK_INDEX] == user_id else "white",
        time_control=game_data.time_control,
        duration_in_ms=game_data.time_in_ms,
    )


@router.post("/games/{user_id}/submit", status_code=status.HTTP_204_NO_CONTENT)
def submit_game(user_id: int, submission_data: GameSubmitData):
    game_data = createGameModel(user_id, submission_data)
    print(f"Adding game data: {game_data}")

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO games (black, white, winner, time_control, duration_in_ms)
                VALUES
                    (
                        :black_player_id,
                        :white_player_id,
                        :winner,
                        :time_control,
                        :time
                    )
                """
            ),
            [
                {
                    "black_player_id": game_data.black,
                    "white_player_id": game_data.white,
                    "winner": game_data.winner,
                    "time_control": game_data.time_control,
                    "time": game_data.duration_in_ms,
                }
            ],
        )


@router.get("/games/{user_id}", response_model=List[GameModel])
def get_history(user_id: int) -> List[GameModel]:
    with db.engine.begin() as connection:
        games = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM games
                WHERE black = :user_id OR white = :user_id
                ORDER BY date_played DESC
                LIMIT 20
                """
            ),
            [{"user_id": user_id}],
        ).all()
    return games


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
