from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, status, HTTPException
from src.api import auth
import sqlalchemy
from src import database as db
from typing import List, Optional
from datetime import date


router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(auth.get_api_key)],
)


class ReportRequest(BaseModel):
    user_id: int
    showcase_id: int = Field(..., ge=-1)
    report_brief: str = Field(..., min_length=1)
    report_details: str | None = Field(..., min_length=1)


class Report(BaseModel):
    user_id: int
    showcase_id: Optional[int]
    report_brief: str = Field(..., min_length=1)
    report_details: str | None = Field(..., min_length=1)
    date_created: date


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_report(report_data: ReportRequest) -> None:
    with db.engine.begin() as connection:
        new_report = connection.execute(
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
                RETURNING report_brief, date_reported
                """
            ),
            {
                "user_id": report_data.user_id,
                "showcase_id": report_data.showcase_id
                if report_data.showcase_id >= 0
                else None,
                "report_brief": report_data.report_brief,
                "report_details": report_data.report_details,
            },
        ).one()
    return {
        "message": "Report successfully sent!",
        "report": new_report.report_brief,
        "created_at": new_report.date_reported,
    }


@router.get("/", response_model=List[Report])
def get_report(report_id: Optional[int] = None):
    with db.engine.begin() as connection:
        if not report_id:
            query = """
                SELECT user_id, showcase_id, report_brief, date_reported, report_details
                FROM reports
            """
        else:
            query = """
                SELECT user_id, showcase_id, report_brief, date_reported, report_details
                FROM reports
                WHERE id = :RId
            """
        results = connection.execute(sqlalchemy.text(query), [{"RId": report_id}]).all()

        if report_id and not results:
            raise HTTPException(
                status_code=404, detail=f"No report found with matching ID: {report_id}"
            )

    return [
        Report(
            user_id=row.user_id,
            showcase_id=row.showcase_id,
            report_brief=row.report_brief,
            date_created=row.date_reported.date(),
            report_details=row.report_details,
        )
        for row in results
    ]
