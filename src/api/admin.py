from fastapi import APIRouter, Depends, status
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)


class AutoWarnResponse(BaseModel):
    affected_users: List[str]


@router.post("/autowarn", response_model=AutoWarnResponse)
def do_autowarn(tolerance: int = 5, user_id: Optional[int] = None):
    """
    Automatically set the status of user(s) with a specific number of recent reports to 'probation'
    """
    with db.engine.begin() as connection:
        if not user_id:
            query = """
                WITH affected_users as (
                    SELECT 
                        user_id
                    FROM reports
                    WHERE
                        ((now()::date - date_reported::date) / 7) < 2
                        AND status IN ('Pending', 'Reviewed')
                    GROUP BY user_id
                    HAVING COUNT(*) >= :tolerance
                )
                UPDATE users
                SET
                    status = 'probation'
                FROM affected_users as au
                WHERE users.id = au.user_id
                RETURNING users.username
            """
            params = {"tolerance": tolerance}
        else:
            query = """
                UPDATE users
                SET status = 'probation'
                WHERE id = :UId AND (
                    SELECT COUNT(*)
                    FROM reports
                    WHERE 
                        user_id = :UId
                        AND ((now()::date - date_reported::date) / 7) < 2
                        AND status IN ('Pending', 'Reviewed')
                ) >= :tolerance
                RETURNING username
            """
            params = {"UId": user_id, "tolerance": tolerance}

        users = connection.execute(sqlalchemy.text(query), params).all()

        return AutoWarnResponse(affected_users=[user.username for user in users])

@router.delete("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_data():
    """
    Truncate all data from all tables; start fresh.
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                TRUNCATE
                    games,
                    reports,
                    showcase_comments,
                    showcase_views,
                    showcases,
                    users
                RESTART IDENTITY
                CASCADE
                """
            )
        )