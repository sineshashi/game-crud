from tortoise.models import Model
from tortoise import fields

class AuthorTable(Model):
    author_id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    email = fields.TextField()

class GameTable(Model):
    game_id = fields.IntField(pk=True)
    authors = fields.ManyToManyField("models.AuthorTable", related_name="published_games")
    name = fields.CharField(max_length=50, null=False, index=True)
    url = fields.TextField()
    published_date = fields.DateField(null=False)