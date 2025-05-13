from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
import sqlalchemy
from src import database as db

from datetime import date

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(auth.get_api_key)],
)


class ReportRequest(BaseModel):
    user_id: int
    showcase_id: int
    report_brief: str
    report_details: str | None


@router.post("/post", status_code=status.HTTP_204_NO_CONTENT)
def post_report(report_data: ReportRequest) -> None:
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO reports (
                    user_id,
                    showcase_id,
                    report_brief,
                    report_details
                )
                VALUES (
                    :user_id,
                    :showcase_id,
                    :report_brief,
                    :report_details
                )
                """
            ),
            {
                "user_id": report_data.user_id,
                "showcase_id": report_data.showcase_id,
                "report_brief": report_data.report_brief,
                "report_details": report_data.report_details,
            },
        )
