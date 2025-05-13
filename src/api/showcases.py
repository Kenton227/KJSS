from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
import sqlalchemy
from src import database as db

from datetime import datetime

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
    date_posted: datetime
    comment_string: str


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
