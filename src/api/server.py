from fastapi import FastAPI
from src.api import (
    games,
    user,
    showcases,
    reports,
)
from starlette.middleware.cors import CORSMiddleware

description = """
The new and upcoming Chess social platform for both serious and casual fans alike!
"""
tags_metadata = [
    {"name": "games", "description": "Games..."},
    {"name": "showcases", "description": "High(/low)lights from games!"},
    {"name": "user", "description": "You're a user, ur a user, everybody's a user"},
    {"name": "reports", "description": "x9 Sion"},
]

app = FastAPI(
    title="Showboard!",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Team KJSS",
        "email": "365teamKJSS@gmail.com",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(games.router)
app.include_router(showcases.router)
app.include_router(user.router)
app.include_router(reports.router)

# app.include_router(inventory.router)
# app.include_router(carts.router)
# app.include_router(catalog.router)
# app.include_router(bottler.router)
# app.include_router(barrels.router)
# app.include_router(admin.router)
# app.include_router(info.router)


@app.get("/")
async def root():
    return {"message": "Shows from the board!"}
