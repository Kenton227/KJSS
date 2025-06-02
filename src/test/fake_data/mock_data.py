import random
from typing import Tuple, List
from datetime import date

import sqlalchemy.exc
from m_title_data import generate_chess_title
from m_captions_data import generate_chess_caption
from m_users_data import generate_fake_users_chunked
from m_comments_data import generate_chess_comment
from m_reports_data import generate_fake_report

import sqlalchemy

from typing import Tuple
import random

import sys
import os

from psycopg import errors

# Add the project root to sys.path for importing database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import src.database as db


# User
def gen_users(desired: int = 100_000) -> None:
    result = generate_fake_users_chunked(desired, 1000)
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO users(username, email, status)
                VALUES
                    (
                        :uname,
                        :email,
                        :stat
                    )
                ON CONFLICT DO NOTHING
                """
            ),
            [
                {
                    "uname": pair[0],
                    "email": pair[1],
                    "stat": random.choices(
                        ["normal", "probation", "banned"], [0.95, 0.02, 0.03]
                    )[0],
                }
                for pair in result
            ],
        )
    print("GENERATE USERS: SUCCESS!")


def gen_random_game(valid_ids: List[int]) -> Tuple:
    black = random.choice(valid_ids)
    white = random.choice(valid_ids)
    while black == white:
        white = random.choice(valid_ids)
    winner = random.choice(["white", "black", "draw"])
    control = random.choice(["classical", "rapid", "blitz", "bullet"])
    duration = random.randint(5000, 1200000)
    date_played = date(
        random.randint(2012, 2025), random.randint(1, 12), random.randint(1, 28)
    )

    # print(black, white, winner, control, duration, date_played)
    return black, white, winner, control, duration, date_played


# Games
def gen_games(desired: int = 150_000) -> None:
    with db.engine.begin() as connection:
        valid_ids = connection.execute(sqlalchemy.text("SELECT id FROM users")).all()

        valid_ids = [valid_id.id for valid_id in valid_ids]

        games = [gen_random_game(valid_ids) for _ in range(desired)]

        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO games(black, white, winner, time_control, duration_in_ms, date_played)
                    VALUES
                        (
                            :black,
                            :white,
                            :winner,
                            :control,
                            :duration,
                            :play_date
                        )
                    ON CONFLICT DO NOTHING
                    """
                ),
                [
                    {
                        "black": game[0],
                        "white": game[1],
                        "winner": game[2],
                        "control": game[3],
                        "duration": game[4],
                        "play_date": game[5],
                    }
                    for game in games
                ],
            )
        except RuntimeError as e:
            print(f"GENERATE GAMES: ERROR {e}")
    print("GENERATE GAMES: SUCCESS!")


def gen_random_sc(valid_uids: List[int], valid_gids: List[int]) -> None:
    author = random.choice(valid_uids)
    title = generate_chess_title()
    caption = generate_chess_caption()
    date_created = date(
        random.randint(2012, 2025), random.randint(1, 12), random.randint(1, 28)
    )
    game = random.choice(valid_gids)
    # print(author, title, caption, date_created, game)
    return author, title, caption, date_created, game


# Showcases
def gen_showcases(desired: int = 150_000) -> None:
    with db.engine.begin() as connection:
        valid_uids = connection.execute(sqlalchemy.text("SELECT id FROM users")).all()

        valid_gids = connection.execute(sqlalchemy.text("SELECT id FROM games")).all()

        valid_uids = [valid_user.id for valid_user in valid_uids]
        valid_gids = [valid_game.id for valid_game in valid_gids]

        showcases = [gen_random_sc(valid_uids, valid_gids) for _ in range(desired)]

        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcases(created_by, title, caption, date_created, game_id)
                    VALUES
                        (
                            :uid,
                            :title,
                            :caption,
                            :date,
                            :game
                        )
                    ON CONFLICT DO NOTHING
                    """
                ),
                [
                    {
                        "uid": sc[0],
                        "title": sc[1],
                        "caption": sc[2],
                        "date": sc[3],
                        "game": sc[4],
                    }
                    for sc in showcases
                ],
            )
        except RuntimeError as e:
            print(f"GENERATE SHOWCASES: ERROR {e}")
    print("GENERATE SHOWCASES: SUCCESS!")


def gen_random_c(valid_scids: List[int], valid_uids: List[int]) -> Tuple:
    author = random.choice(valid_uids)
    sc = random.choice(valid_scids)
    comment = generate_chess_comment()
    # print(author, sc, comment)
    return author, sc, comment


# Showcase comments
def gen_comments(desired: int = 250_000) -> None:
    with db.engine.begin() as connection:
        valid_uids = connection.execute(sqlalchemy.text("SELECT id FROM users")).all()

        valid_sids = connection.execute(
            sqlalchemy.text("SELECT id FROM showcases")
        ).all()

        valid_uids = [valid_user.id for valid_user in valid_uids]
        valid_sids = [valid_game.id for valid_game in valid_sids]

        comments = [gen_random_c(valid_sids, valid_uids) for _ in range(desired)]

        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_comments(author_id, showcase_id, comment)
                    VALUES
                        (
                            :uid,
                            :sid,
                            :comment
                        )
                    ON CONFLICT DO NOTHING
                    """
                ),
                [{"uid": c[0], "sid": c[1], "comment": c[2]} for c in comments],
            )
        except RuntimeError as e:
            print(f"GENERATE COMMENTS: ERROR {e}")
    print("GENERATE COMMENTS: SUCCESS!")


def gen_random_v(valid_scids: List[int], valid_uids: List[int]) -> Tuple:
    author = random.choice(valid_uids)
    sc = random.choice(valid_scids)
    liked = False if random.randint(0, 2) else True
    # print(author, sc, liked)
    return author, sc, liked


# Showcase views
def gen_views(desired: int = 300_000) -> None:
    with db.engine.begin() as connection:
        valid_uids = connection.execute(sqlalchemy.text("SELECT id FROM users")).all()

        valid_sids = connection.execute(
            sqlalchemy.text("SELECT id FROM showcases")
        ).all()

        valid_uids = [valid_user.id for valid_user in valid_uids]
        valid_sids = [valid_game.id for valid_game in valid_sids]

        views = [gen_random_v(valid_sids, valid_uids) for _ in range(desired)]

        try:
            # Insert liked views
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_views(showcase_id, user_id, liked, view_timestamp, liked_timestamp)
                    VALUES
                        (
                            :sid,
                            :uid,
                            :liked,
                            DEFAULT,
                            DEFAULT)
                    ON CONFLICT DO NOTHING
                    """
                ),
                [{"sid": v[1], "uid": v[0], "liked": v[2]} for v in views if v[2]],
            )

            # Insert unliked views
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_views(showcase_id, user_id, liked, view_timestamp)
                    VALUES
                        (
                            :sid,
                            :uid,
                            :liked,
                            DEFAULT)
                    ON CONFLICT DO NOTHING
                    """
                ),
                [{"sid": v[1], "uid": v[0], "liked": v[2]} for v in views if not v[2]],
            )

        except RuntimeError as e:
            print(f"GENERATE VIEWS: ERROR {e}")
    print("GENERATE VIEWS: SUCCESS!")


# Reports
def gen_random_r(id_pairs: List[Tuple[int]]) -> Tuple:
    sinner, sc = random.choice(id_pairs)
    brief, detail = generate_fake_report()
    status = random.choice(["pending", "reviewed", "dismissed"])

    # print(sinner, sc, brief, detail, status)
    return sinner, sc, brief, detail, status


def gen_reports(desired: int = 50_000) -> None:
    with db.engine.begin() as connection:
        valid_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT DISTINCT
                    u.id as uid, 
                    s.id as sid
                FROM users as u
                JOIN showcases as s
                    on s.created_by = u.id
                """
            )
        ).all()

        valid_id_pairs = [(valid_user.uid, valid_user.sid) for valid_user in valid_ids]

        reports = [gen_random_r(valid_id_pairs) for _ in range(desired)]

        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO reports(user_id, showcase_id, report_brief, report_details, status)
                    VALUES
                        (
                            :uid,
                            :sid,
                            :brief,
                            :details,
                            :status
                        )
                    ON CONFLICT DO NOTHING
                    """
                ),
                [
                    {
                        "uid": r[0],
                        "sid": r[1],
                        "brief": r[2],
                        "details": r[3],
                        "status": r[4],
                    }
                    for r in reports
                ],
            )
        except RuntimeError as e:
            print(f"GENERATE REPORTS: ERROR {e}")
    print("GENERATE REPORTS: SUCCESS!")


if __name__ == "__main__":
    print("hello world")

    gen_users()

    gen_games()

    gen_showcases()

    gen_comments()

    gen_views()

    gen_reports()
