from tortoise.models import Model
from tortoise import fields, Tortoise
import datetime

class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='comments')
    post = fields.ForeignKeyField('models.Post', related_name='comments')

    def __str__(self):
        return self.content