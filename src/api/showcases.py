from pydantic import BaseModel, model_validator, Field
from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy.exc
from src.api import auth
import sqlalchemy
from src import database as db
from typing import Self, Optional
from psycopg import errors

from datetime import datetime

router = APIRouter(
    prefix="/showcases",
    tags=["showcases"],
    dependencies=[Depends(auth.get_api_key)],
)


class ShowcaseRequest(BaseModel):
    user_id: int
    title: str = Field(..., min_length=1)
    game_id: int
    caption: Optional[str]


class EditRequest(BaseModel):
    title: str = Field(..., min_length=1)
    caption: Optional[str]

    @model_validator(mode="after")
    def check_empty_request(self) -> Self:
        if self.title == "" and self.caption == "":
            raise ValueError("must update at least title or caption")
        return self



class Comment(BaseModel):
    post_id: int
    auther_id: int
    date_posted: datetime
    comment_string: str = Field(..., min_length=1)


@router.post("/post", status_code=status.HTTP_204_NO_CONTENT)
def post_showcase(showcase_data: ShowcaseRequest) -> None:
    with db.engine.begin() as connection:
        try:
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
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                if "games" in e.orig.__str__():
                    raise HTTPException(
                        status_code=404,
                        detail="Referenced game ID does not exist"
                    )
                if "users" in e.orig.__str__():
                    raise HTTPException(
                        status_code=404,
                        detail="Referenced user ID does not exist"
                    )


@router.post("/edit/{showcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_showcase(showcase_id: int, new_data: EditRequest) -> None:
    with db.engine.begin() as connection:
        title_confirm = None
        caption_confirm = None
        if new_data.title != "":
            title_confirm = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE showcases
                        SET
                            title = :new_title
                        WHERE id = :id
                    RETURNING id;
                    """
                ),
                [{"id": showcase_id, "new_title": new_data.title}],
            ).one_or_none()
        if new_data.caption != "":
            caption_confirm = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE showcases
                        SET
                            caption = :new_caption
                        WHERE id = :id
                    RETURNING id;
                    """
                ),
                [{"id": showcase_id, "new_caption": new_data.caption}],
            ).one_or_none()
        if not title_confirm and not caption_confirm:
            raise HTTPException(
                status_code=404,
                detail=f"No showcase found with id: {showcase_id}"
            )


@router.post("/{showcase_id}/comment", status_code=status.HTTP_204_NO_CONTENT)
def post_comment(comment_content: Comment, showcase_id: int):
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
                    "author_id": comment_content.auther_id,
                    "showcase_id": showcase_id,
                    "comment": comment_content.comment_string,
                },
            )
