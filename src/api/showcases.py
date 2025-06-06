from pydantic import BaseModel, model_validator, Field
from fastapi import APIRouter, Depends, status, HTTPException
import sqlalchemy.exc
from src.api import auth
from typing import List
import sqlalchemy
from src import database as db
from typing import Self, Optional, List
from psycopg import errors

from datetime import datetime
from src.db.schemas import Showcase
from datetime import date
from enum import Enum

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


class NewComment(BaseModel):
    author_id: int
    date_posted: datetime
    comment_string: str = Field(..., min_length=1)


class Comment(BaseModel):
    comment_id: int
    author: str = Field(..., min_length=1)
    date_posted: datetime
    content: str = Field(..., min_length=1)

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class ShowcasesSortOptions(str, Enum):
    title = "title"
    view_count = "view_count"
    like_count = "like_count"
    date_created = "date_created"


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_showcase(showcase_data: ShowcaseRequest) -> None:
    """
    Post a showcase to the database.
    Showcases must be linked to an existing user ID.
    If a title is not provided, the showcase will have the default value: "Untitled".
    A caption is unnecessary.
    """
    with db.engine.begin() as connection:
        try:
            new_showcase = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcases (created_by, game_id, title, caption)
                    VALUES (
                        :user_id,
                        :game_id,
                        :title,
                        :caption
                    )
                    RETURNING id, title, date_created
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
            ).one()
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                if "games" in e.orig.__str__():
                    raise HTTPException(
                        status_code=404, detail="Referenced game ID does not exist"
                    )
                if "users" in e.orig.__str__():
                    raise HTTPException(
                        status_code=404, detail="Referenced user ID does not exist"
                    )
    return {
        "message": "New showcase created!",
        "showcase_id": new_showcase.id,
        "title": new_showcase.title,
        "date_created": new_showcase.date_created,
    }


@router.put("/{showcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_showcase(showcase_id: int, new_data: EditRequest) -> None:
    """
    Edits the string content of a showcase given by ID.
    'String content' includes the title and/or caption.
    If the provided title/caption is empty, it the current value will remain unaltered.
    An empty edit (lacks new title and new caption) will return an error.
    """
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
                status_code=404, detail=f"No showcase found with id: {showcase_id}"
            )


@router.post("/{showcase_id}/comment", status_code=status.HTTP_201_CREATED)
def post_comment(comment_content: NewComment, showcase_id: int):
    """
    Add a new comment to a specific showcase specified by ID.
    Comments cannot be empty.
    Comments must reference a valid user by ID.
    """
    with db.engine.begin() as connection:
        # makes sure comment string isn't empty
        if comment_content.comment_string == "":
            raise HTTPException(status_code=422, detail="Comment is empty")

        try:
            new_comment = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_comments (author_id, showcase_id, comment)
                    VALUES (
                    :author_id,
                    :showcase_id,
                    :comment
                    )
                    RETURNING post_id, author_id, comment, created_at
                    """
                ),
                {
                    "author_id": comment_content.author_id,
                    "showcase_id": showcase_id,
                    "comment": comment_content.comment_string,
                },
            ).one()
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                if "users" in e.orig.__str__():
                    raise HTTPException(status_code=422, detail="Bad user reference")
                elif "showcases" in e.orig.__str__():
                    raise HTTPException(
                        status_code=422, detail="Bad showcase reference"
                    )
                else:
                    raise e
    return {
        "message": "Comment successfully sent!",
        "comment_id": new_comment.post_id,
        "author_uid": new_comment.author_id,
        "comment": new_comment.comment,
        "time_sent": new_comment.created_at,
    }


@router.get("/{showcase_id}/comments", response_model=List[Comment])
def get_comments(showcase_id: int):
    """
    Retrieve all comments on a showcase specified by ID.
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT post_id, username, comment, created_at
                FROM showcase_comments as sc
                JOIN users as u on sc.author_id = u.id
                WHERE showcase_id = :SId
                """
            ),
            [{"SId": showcase_id}],
        ).all()

        if not result:
            showcase_exists = connection.execute(
                sqlalchemy.text("SELECT 1 FROM showcases where id = :SId"),
                {"SId": showcase_id},
            ).one_or_none()
            if not showcase_exists:
                raise HTTPException(status_code=404, detail="No showcase found")

    return [
        Comment(
            comment_id=row.post_id,
            author=row.username,
            date_posted=row.created_at,
            content=row.comment
        )
        for row in result
    ]


@router.delete("/{showcase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_showcase(showcase_id: int):
    """
    Delete a showcase from the database, specified by ID.
    Attached comments will also be deleted.
    """
    with db.engine.begin() as connection:
        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    DELETE FROM showcases
                        WHERE id = :SId
                    RETURNING id
                    """
                ),
                [{"SId": showcase_id}],
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Showcase not found")


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int):
    """
    Delete a comment, specified by ID.
    """
    with db.engine.begin() as connection:
        try:
            connection.execute(
                sqlalchemy.text(
                    """
                    DELETE FROM showcase_comments
                        WHERE post_id = :CId
                    RETURNING post_id
                    """
                ),
                [{"CId": comment_id}],
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Comment not found")


@router.post("/view/{showcase_id}", status_code=status.HTTP_201_CREATED)
def view_showcase(showcase_id: int, user_id: int):
    """
    Adds a view from a user to a showcase, specified by ID.
    """
    with db.engine.begin() as connection:
        try:
            result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO showcase_views (showcase_id, user_id, liked_timestamp)
                    VALUES (:SId, :UId, NULL)
                    ON CONFLICT
                        DO NOTHING
                    RETURNING id
                    """
                ),
                {"SId": showcase_id, "UId": user_id},
            ).one_or_none()

            if not result:
                raise HTTPException(status_code=208, detail="Already viewed")
            else:
                return {
                    "message": f"User ID: {user_id} successfully viewed Showcase ID: {showcase_id}"
                }
        except sqlalchemy.exc.IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                raise HTTPException(status_code=404, detail="Cannot find ID(s)")


@router.put("/like/{showcase_id}", status_code=status.HTTP_200_OK)
def like_showcase(showcase_id: int, user_id: int):
    """
    Add a like from a user to a showcase, specified by ID.
    A user needs to have viewed a showcase before liking it.
    There is no way to un-like a showcase.
    """
    with db.engine.begin() as connection:
        try:
            result = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE showcase_views
                    SET
                        liked = True,
                        liked_timestamp = now()
                    WHERE
                        showcase_id = :SId
                        AND user_id = :UId
                        AND liked = False
                    RETURNING id
                    """
                ),
                {"SId": showcase_id, "UId": user_id},
            ).one()

            if not result:
                raise HTTPException(status_code=208, detail="Already liked")
            else:
                return {
                    "message": f"User ID: {user_id} successfully liked Showcase ID: {showcase_id}"
                }
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Cannot find ID(s)")


@router.get("/search", response_model=List[Showcase])
def search_all_showcases(
        user_query: str = "",
        sc_query: str = "",
        sort_col: ShowcasesSortOptions = ShowcasesSortOptions.date_created,   
        sort_order: SortOrder = SortOrder.desc
    ):
    """
    Retrieves showcases that match the following optional queries:
    - user_query: Searches showcases based on the author's username; shows results that contain query as a substring of the username.
    - sc_query:  Searches text content (title and caption); shows results that contain query as a substring of either attributes.

    Any empty query will not result in any filration of the data by that query.
    """
    with db.engine.begin() as connection:
        results = connection.execute(
            sqlalchemy.text(
                f"""
                    WITH views as (
                        SELECT showcase_id, COUNT(*) as view_count
                        FROM showcase_views
                        GROUP BY showcase_id
                    ),
                    likes as (
                        SELECT showcase_id, COUNT(*) as like_count
                        FROM showcase_views
                        WHERE liked = True
                        GROUP BY showcase_id
                    )
                    SELECT
                        s.id as id,
                        u.username as author,
                        title,
                        COALESCE(view_count, 0) as view_count,
                        COALESCE(like_count, 0) as like_count,
                        caption,
                        date_created,
                        game_id
                    FROM showcases as s
                    JOIN users as u on s.created_by = u.id
                    LEFT JOIN views as v on s.id = v.showcase_id
                    LEFT JOIN likes as l on s.id = l.showcase_id
                    WHERE
                        (title ILIKE '%' || :sc_query || '%'
                            OR caption ILIKE '%' || :sc_query || '%')
                        AND (u.username ILIKE '%' || :u_query || '%')
                    ORDER BY {sort_col.value} {sort_order.value}
                """
            ),
            {"u_query": user_query, "sc_query": sc_query},
        ).all()

    return [
        Showcase(
            showcase_id=row.id,
            created_by=row.author,
            title=row.title,
            views=row.view_count,
            likes=row.like_count,
            caption=row.caption,
            date_created=row.date_created,
            game_id=row.game_id,
        )
        for row in results
    ]


@router.get("/{showcase_id}", response_model=Showcase)
def get_showcase(showcase_id: int):
    """
    Retrieve a specific showcase by ID.
    """
    with db.engine.begin() as connection:
        try:
            result = connection.execute(
                sqlalchemy.text(
                    """
                    WITH views as (
                        SELECT showcase_id, COUNT(*) as view_count
                        FROM showcase_views
                        GROUP BY showcase_id
                    ),
                    likes as (
                        SELECT showcase_id, COUNT(*) as like_count
                        FROM showcase_views
                        WHERE liked = True
                        GROUP BY showcase_id
                    )
                    SELECT
                        s.id as id,
                        u.username as author,
                        title,
                        view_count,
                        like_count,
                        caption,
                        date_created,
                        game_id
                    FROM showcases as s
                    JOIN views as v on s.id = v.showcase_id
                    JOIN likes as l on s.id = l.showcase_id
                    JOIN users as u on u.id = s.created_by
                    WHERE s.id = :showcase_id
                    ORDER BY date_created DESC
                    """
                ),
                {"showcase_id": showcase_id},
            ).one()

            return Showcase(
                showcase_id=result.id,
                created_by=result.author,
                title=result.title,
                views=result.view_count,
                likes=result.like_count,
                caption=result.caption,
                date_created=result.date_created,
                game_id=result.game_id,
            )
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(
                status_code=404, detail=f"No showcase found"
            )
