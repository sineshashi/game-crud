import datetime
from typing import Optional, List, Type, Dict
from tortoise.transactions import atomic

from .models import GameTable, AuthorTable
from .exceptions import ValidationException, NoContentException


class Author:
    '''This class holds the properties of authors and their methods.'''
    _table = AuthorTable

    def __init__(
        self,
        first_name: str,
        last_name: str,
        author_id: Optional[int] = None,
        orm_obj: Optional[AuthorTable] = None
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.author_id = author_id
        self.orm_obj = orm_obj

    def dict(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "author_id": self.author_id
        }

    def _dict(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    async def save(self) -> None:
        '''Saves the author in db. If needed, it creates it otherwise updates it.'''
        if self.author_id is None:
            created_obj = await self._table.create(**self._dict())
            self.author_id = created_obj.author_id
            self.orm_obj = created_obj
        else:
            await self._table.filter(author_id=self.author_id).update(**self._dict())

    @classmethod
    async def filter(cls: "Type[Author]", **kwargs) -> List["Author"]:
        '''Filter authors based on kwargs passed.'''
        orm_instances = await cls._table.filter(**kwargs)
        return [
            cls(
                first_name=obj.first_name,
                last_name=obj.last_name,
                author_id=obj.author_id,
                orm_obj=obj
            ) for obj in orm_instances
        ]

    @classmethod
    async def all(cls: "Type[Author]") -> List["Author"]:
        '''Returns all authors in db.'''
        orm_instances = await cls._table.all()
        return [
            cls(
                first_name=obj.first_name,
                last_name=obj.last_name,
                author_id=obj.author_id,
                orm_obj=obj
            ) for obj in orm_instances
        ]

    @classmethod
    def orm_to_obj(cls: "Type[Author]", orm_obj: "Author._table") -> "Author":
        '''Converts orm obj to our obj.'''
        return cls(
            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            author_id=orm_obj.author_id,
            orm_obj=orm_obj
        )


class Game:
    '''This class holds the fields and methods of Game.'''
    _table = GameTable

    def __init__(
        self,
        name: str,
        url: str,
        published_date: datetime,
        game_id: Optional[int] = None,
        orm_obj: Optional[GameTable] = None,
    ) -> None:
        self.name = name
        self.url = url
        self.published_date = published_date
        self.game_id = game_id
        self.orm_obj = orm_obj

    def dict(self) -> Dict:
        return {
            "name": self.name,
            "url": self.url,
            "published_date": self.published_date,
            "game_id": self.game_id
        }

    def _dict(self) -> Dict:
        return {
            "name": self.name,
            "url": self.url,
            "published_date": self.published_date
        }

    async def save(self) -> None:
        if self.game_id is None:
            created_obj = await self._table.create(**self._dict())
            self.game_id = created_obj.game_id
            self.orm_obj = created_obj
        else:
            await self._table.filter(game_id=self.game_id).update(**self._dict())

    @classmethod
    def _orm_to_obj(cls: "Type[Game]", orm_obj: "Type[Game._table]") -> "Game":
        return cls(
            name=orm_obj.name,
            url=orm_obj.url,
            published_date=orm_obj.published_date,
            game_id=orm_obj.game_id,
            orm_obj=orm_obj
        )

    @classmethod
    async def get(cls: "Type[Game]", **kwargs) -> "Optional[Game]":
        orm_obj = await cls._table.filter(**kwargs).prefetch_related("authors").first()
        if orm_obj is None:
            return orm_obj
        return cls._orm_to_obj(orm_obj=orm_obj)

    @classmethod
    async def all(cls: "Type[Game]") -> "List[Game]":
        orm_objs = await cls._table.all().prefetch_related("authors")
        return [cls._orm_to_obj(orm_obj) for orm_obj in orm_objs]

    @classmethod
    async def delete(cls: "Type[Game]", **kwargs) -> None:
        await cls._table.filter(**kwargs).delete()


class GameAuthorConnector:
    def __init__(self, game: Game, authors: List[Author]) -> None:
        self.game = game
        self.authors = authors

    def dict(self) -> Dict:
        d = self.game.dict()
        d["authors"] = [author.dict() for author in self.authors]
        return d

    @classmethod
    async def get_authors_from_game(cls: "Type[GameAuthorConnector]", game: Game) -> "GameAuthorConnector":
        '''Get authors of a game.'''
        if game.orm_obj is None:
            game = await Game.get(game_id=game.game_id)
        author_orm_objs = await game.orm_obj.authors.all()
        return cls(
            game=game,
            authors=[
                Author.orm_to_obj(orm_obj) for orm_obj in author_orm_objs
            ]
        )

    @classmethod
    async def add_authors_to_game(cls: "Type[GameAuthorConnector]", game: Game, authors: List[Author]):
        '''Add new authors to a game.'''
        await game.orm_obj.authors.add(*[
            obj.orm_obj for obj in authors
        ])

    async def create(self: "GameAuthorConnector", author_ids: List[int]) -> "GameAuthorConnector":
        '''
        Creates game and creates authors in the self.authors as well as fetches authors from ids.
        Then adds all the authors to the game.
        '''
        @atomic()
        async def _create():
            filtered_authors = await Author.filter(author_id__in=author_ids)
            if len(filtered_authors) != len(author_ids):
                raise ValidationException(
                    field="author_ids", error="Some field is wrong.")

            await self.game.save()
            for author in self.authors:
                await author.save()
            self.authors.extend(filtered_authors)
            await self.add_authors_to_game(self.game, self.authors)
            return self
        return await _create()

    @classmethod
    async def get(cls: "Type[GameAuthorConnector]", **kwargs) -> "GameAuthorConnector":
        game = await Game.get(**kwargs)
        if game is None:
            raise NoContentException(detail="Game not found.")

        return await cls.get_authors_from_game(game)

    @classmethod
    async def all(cls: "Type[GameAuthorConnector]") -> "List[GameAuthorConnector]":
        games = await Game.all()
        return [await cls.get_authors_from_game(game) for game in games]

    @classmethod
    async def delete(cls: "Type[GameAuthorConnector]", **kwargs) -> None:
        await Game.delete(**kwargs)

    @classmethod
    async def update_game(cls: "Type[GameAuthorConnector]", **kwargs) -> Dict:
        game = Game(**kwargs)
        await game.save()
        return game.dict()
