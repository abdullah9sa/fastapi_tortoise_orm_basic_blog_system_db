from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, create_model


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='posts')
    category = fields.CharField(max_length=255)

    def __str__(self):
        return self.title