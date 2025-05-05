from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)
