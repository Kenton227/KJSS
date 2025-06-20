from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import APIRouter, Depends, status, Query, HTTPException
import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Self, Optional

from datetime import date, datetime
from psycopg import errors
from src.db.schemas import Color, GameStatus, TimeControl, GameModel, Showcase

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)


class GameSubmitData(BaseModel):
    color: Color
    game_status: GameStatus
    time_control: TimeControl
    opponent_id: int
    time_in_ms: int = Field(ge=0, description="Time must be non-zero and non-negative")
    date_played: date


class UserViews(BaseModel):
    username: str
    email: Optional[str]
    avg_views: float
    total_likes: int


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
        id=-1,
        black=black_player,
        white=white_player,
        winner=winner,
        time_control=game_data.time_control,
        duration_in_ms=game_data.time_in_ms,
        date_played=game_data.date_played,
    )

class User(BaseModel):
    user_id: int
    username: str
    email: Optional[str]
    date_registered: datetime
    status: str 

@router.get("/{user_id}", response_model=User)
def get_user(user_id):
    """Retrieve a user by ID."""
    with db.engine.begin() as connection:
        try:
            user = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT
                        id, username, email, register_date, status
                    FROM users as u
                    WHERE id = :uid
                    """
                ),
                {"uid": user_id}
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(
                status_code=404, detail=f"No user found"
            )
    return User(
        user_id= user.id,
        username=user.username,
        email=user.email,
        date_registered=user.register_date,
        status=user.status
    )

@router.post("/games/{user_id}", status_code=status.HTTP_201_CREATED)
def submit_game(user_id: int, submission_data: GameSubmitData):
    """
    Users can submit their games into record.
    Games are submitted from the user's perspective, taking in their color played and whether or not they win/lose.
    The opponent's id must be different than the user's own.
    """
    game_data = create_game_model(user_id, submission_data)
    print(f"Adding game data: {game_data}")

    with db.engine.begin() as connection:
        try:
            new_id = connection.execute(  # Inserting a duplicate game will return the existing game ID (No actual way to proc a unique violation tho)
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
                        "date": game_data.date_played,
                    }
                ],
            ).one()
        except sqlalchemy.exc.IntegrityError as e:  # Catch foreign key violations
            if isinstance(e.orig, errors.ForeignKeyViolation):
                raise HTTPException(status_code=422, detail=f"Bad player IDs")
    return {
        "message": f"New game added to user ID: {user_id}",
        "new_game_id": new_id.id,
    }


@router.get("/games/{user_id}", response_model=List[GameModel])
def get_game_history(user_id: int) -> List[GameModel]:
    """
    Retrieve the last 20 games recorded involving specific user.
    Response is sorted by date starting with most recent.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT
                    id,
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

        if (
            not result
        ):  # If empty result, check if its because there's no user or user has no games
            user_confirm = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT id
                    FROM users
                    WHERE id = :user_id
                    """
                ),
                [{"user_id": user_id}],
            ).one_or_none()

            if not user_confirm:
                raise HTTPException(status_code=404, detail=f"User does not exist")
            raise HTTPException(
                status_code=404, detail=f"User has not recorded any games"
            )

    return [
        GameModel(
            game_id=row.id,
            black=row.black,
            white=row.white,
            winner=row.winner if row.winner != 'draw' else None,
            time_control=row.time_control,
            duration_in_ms=row.duration_in_ms,
            date_played=row.date_played,
        )
        for row in result
    ]


@router.get("/showcases/{user_id}", response_model=List[Showcase])
def get_user_showcases(user_id: int) -> List[Showcase]:
    """
    Get all showcases posted by a specific user.
    Response is sorted by most recently created.
    """
    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                """
                SELECT created_by, title, caption, date_created, game_id
                FROM showcases
                WHERE created_by = :user_id
                ORDER BY date_created DESC
                """
            ),
            {"user_id": user_id},
        ).all()
    return [
        Showcase(
            created_by=row.created_by,
            title=row.title,
            caption=row.caption,
            date_created=row.date_created,
            game_id=row.game_id,
        )
        for row in results
    ]


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(username: str, user_email: Optional[str] = Query(default=None)):
    """
    Register a new user into the database.
    A username is required, an email is optional.
    Usernames and emails must be unique from all others stored, if not a 422 error will be returned.
    """
    with db.engine.begin() as connection:
        try:
            new_user = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO users(username, email, register_date)
                    VALUES
                        (:username, LOWER(:user_email), DEFAULT)
                    RETURNING id, register_date
                    """
                ),
                {"username": username, "user_email": user_email},
            ).one()
        except (
            sqlalchemy.exc.IntegrityError
        ) as e:  # Return a warning if user/email already exists
            if isinstance(e.orig, errors.UniqueViolation):
                raise HTTPException(
                    status_code=422, detail="User or email already in use"
                )

    return {
        "message": f"New user registered!",
        "uid": new_user.id,
        "username": username,
        "email": user_email,
        "registered_at": new_user.register_date,
    }


@router.get("/trending", response_model=List[UserViews])
def get_trending_users(top_n: int, week_range: int):
    """Find the top 'top_n' users who have gotten the most views & likes in the last 'week_range' weeks"""
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                WITH view_data as (
                    SELECT
                        s.id as showcase_id,
                        COALESCE(COUNT(sv.id), 0) as views
                    FROM showcases as s
                    LEFT JOIN showcase_views as sv on s.id = sv.showcase_id
                    WHERE (now()::date - sv.view_timestamp::date)/7 <= :range
                    GROUP BY s.id
                ),
                avg_views as (
                    SELECT
                        s.created_by as user_id,
                        COALESCE(AVG(vd.views), 0) as avg_views
                    FROM showcases as s
                    LEFT JOIN view_data as vd on s.id = vd.showcase_id
                    GROUP BY s.created_by
                ),
                total_likes as (
                    SELECT
                        s.created_by as user_id,
                        COALESCE(COUNT(sv.liked), 0) as total_likes
                    FROM showcases as s
                    LEFT JOIN showcase_views as sv on sv.showcase_id = s.id
                    WHERE (now()::date - sv.liked_timestamp::date)/7 <= :range
                        AND sv.liked = True
                    GROUP BY s.created_by
                )
                SELECT
                    u.username,
                    u.email,
                    COALESCE(av.avg_views, 0) as avg_views,
                    COALESCE(tl.total_likes, 0) as total_likes
                FROM users as u
                LEFT JOIN avg_views as av on u.id = av.user_id
                left JOIN total_likes as tl on u.id = tl.user_id
                ORDER BY total_likes DESC, avg_views DESC
                LIMIT :n
                """
            ),
            {"range": week_range, "n": top_n},
        ).all()

    return [
        UserViews(
            username=row.username,
            email=row.email,
            avg_views=row.avg_views,
            total_likes=row.total_likes,
        )
        for row in result
    ]
