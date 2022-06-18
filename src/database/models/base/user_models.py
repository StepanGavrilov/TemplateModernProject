from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(
        pk=True
    )
    name = fields.CharField(
        max_length=128
    )
    age = fields.CharField(
        max_length=128
    )
