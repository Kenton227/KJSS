from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
from typing import List
import sqlalchemy
from src import database as db

from datetime import date

router = APIRouter(
    prefix="/showcases",
    tags=["showcases"],
    dependencies=[Depends(auth.get_api_key)],
)


class ShowcaseRequest(BaseModel):
    user_id: str
    title: str
    game_id: int
    caption: str


class EditRequest(BaseModel):
    title: str
    caption: str


class comment(BaseModel):
    post_id: int
    auther_uid: int
    date_posted: date
    comment_string: str


class showcase_search_result(BaseModel):
    showcase_id: int
    user_id: int
    title: str
    date_created: date
    caption: str


@router.post("/post", status_code=status.HTTP_204_NO_CONTENT)
def post_showcase(showcase_data: ShowcaseRequest) -> None:
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO showcases (created_by, game_id, title, caption)
                VALUES (
                    :user_id,
                    :game_id,
                    :title,
                    :caption
                )
                """
            ),
            [
                {
                    "user_id": showcase_data.user_id,
                    "game_id": showcase_data.game_id,
                    "title": showcase_data.title,
                    "caption": showcase_data.caption,
                }
            ],
        )


@router.post("/edit/{showcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_showcase(showcase_id: int, new_data: EditRequest) -> None:
    with db.engine.begin() as connection:
        if new_data.title != "":
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE showcases
                        SET
                            title = :new_title
                        WHERE id = :id
                    """
                ),
                [{"id": showcase_id, "new_title": new_data.title}],
            )
        if new_data.caption != "":
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE showcases
                        SET
                            caption = :new_caption
                        WHERE id = :id
                    """
                ),
                [{"id": showcase_id, "new_caption": new_data.caption}],
            )


@router.post("/{showcase_id}/comment", status_code=status.HTTP_204_NO_CONTENT)
def post_comment(comment_content: comment, showcase_id: int):
    with db.engine.begin() as connection:
        # makes sure comment string isn't empty
        if comment_content.comment_string != "":
            connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_comments (post_id, author_id, showcase_id, comment)
                    VALUES (
                    :post_id,
                    :author_id,
                    :showcase_id,
                    :comment
                    )
                    """
                ),
                {
                    "post_id": comment_content.post_id,
                    "author_id": comment_content.auther_uid,
                    "showcase_id": showcase_id,
                    "comment": comment_content.comment_string,
                },
            )
@router.get("/search", status_code=status.HTTP_200_OK,
    response_model=List[showcase_search_result],)
def search_showcase(input_title: str, input_author_name: str):
    with db.engine.begin() as connection:
        search = connection.execute(
            sqlalchemy.text(
                """
                SELECT showcases.id AS showcase_id, created_by AS user_id, users.username AS username, title, date_created, caption
                FROM showcases
                JOIN users ON showcases.created_by = users.id
            
                """
            )
        ).mappings().all()

        matched: List[showcase_search_result] = []
        for row in search:
            if row["title"] == input_title or row["username"] == input_author_name:
                showcase = showcase_search_result(
                showcase_id=row["showcase_id"],
                user_id=row["user_id"],
                username=row["username"],
                title=row["title"],
                date_created=row["date_created"],
                caption=row["caption"]
            )
                matched.append(showcase)
        return matched