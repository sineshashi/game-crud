from fastapi import APIRouter
from typing import List

from .datatypes import GameDataTypeIn, GameDataTypeOut, SuccessResponse, GameUpdateDataTypeIn, \
    GameUpdateDataTypeOut, AuthorDataTypeOut
from .core import GameAuthorConnector, Game, Author

router = APIRouter()


@router.post("/createGame", response_model=GameDataTypeOut)
async def create_game(
    game: GameDataTypeIn
):
    game_instance = Game(
        name=game.name,
        url=game.url,
        published_date=game.published_date
    )
    authors = [
        Author(
            first_name=obj.first_name,
            last_name=obj.last_name,
        ) for obj in game.authors
    ]
    return (await GameAuthorConnector(
        game=game_instance, authors=authors
    ).create(game.author_ids)).dict()


@router.get("/getGame/{game_id}", response_model=GameDataTypeOut)
async def get_game(
    game_id: str
):
    return (await GameAuthorConnector.get(game_id=game_id)).dict()


@router.get("/allGames", response_model=List[GameDataTypeOut])
async def all_games():
    return [
        obj.dict() for obj in await GameAuthorConnector.all()
    ]


@router.delete("/deleteGame/{game_id}", response_model=SuccessResponse)
async def delete_game(game_id: int):
    await GameAuthorConnector.delete(game_id=game_id)
    return {"success": True}


@router.put("/updateGame/{game_id}", response_model=GameUpdateDataTypeOut)
async def update_game(
    game_id: int,
    game: GameUpdateDataTypeIn
):
    return await GameAuthorConnector.update_game(game_id=game_id, **game.dict())

@router.get("/allAuthors", response_model=List[AuthorDataTypeOut])
async def all_authors():
    return [
        obj.dict() for obj in await Author.all()
    ]