from tortoise import fields
from tortoise.models import Model


class Profile(Model):
    name = fields.CharField(max_length=128)
