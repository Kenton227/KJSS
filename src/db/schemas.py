from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Self
from datetime import date


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
    likes: int
    caption: str
    date_created: date
    game_id: int
