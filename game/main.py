from fastapi import FastAPI
from tortoise import generate_config
from tortoise.contrib.fastapi import register_tortoise
from .config import DBURL
import game.controller as api_router

app = FastAPI()

db_config = generate_config(
    db_url=DBURL,
    app_modules={
        "models": ["game.models", "aerich.models"]
    }
)

register_tortoise(
    app=app,
    config=db_config,
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(
    router=api_router.router,
)
