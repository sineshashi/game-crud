from pydantic import BaseModel, validator
import validators
import datetime
from typing import List

from .exceptions import ValidationException


class AuthorDataTypeIn(BaseModel):
    first_name: str
    last_name: str

class GameDataTypeIn(BaseModel):
    name: str
    url: str
    published_date: datetime.date
    author_ids: List[int] = []
    authors: List[AuthorDataTypeIn]

    @validator("url")
    def validate_url(cls, v, values):
        if validators.url(v):
            return v
        raise ValidationException(field="url", error="Invalid")

    @validator("authors")
    def validate_authors(cls, v, values):
        if len(values["author_ids"]) == 0 and len(v) == 0:
            raise ValidationException(
                field="authors", error="Both author and author_ids can not be empty.")
        return v

    @validator("published_date")
    def validate_date(cls, v):
        if v > datetime.datetime.now().date():
            raise ValidationException(
                field="published_date", error="Published date is greater than today.")
        return v


class AuthorDataTypeOut(BaseModel):
    author_id: int
    first_name: str
    last_name: str


class GameDataTypeOut(BaseModel):
    game_id: int
    name: str
    url: str
    published_date: datetime.date
    authors: List[AuthorDataTypeOut]


class SuccessResponse(BaseModel):
    success: bool


class GameUpdateDataTypeIn(BaseModel):
    name: str
    url: str
    published_date: datetime.date

    @validator("url")
    def validate_url(cls, v, values):
        if validators.url(v):
            return v
        raise ValidationException(field="url", error="Invalid")


class GameUpdateDataTypeOut(GameUpdateDataTypeIn):
    game_id: int
