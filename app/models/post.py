from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, create_model
import datetime
from app.models.user import UserOutResponse
from typing import List
from typing import Optional
from app.models.user import User

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='posts')
    category = fields.CharField(max_length=255)

# Pydantic models for input and output
PostInResponse = pydantic_model_creator(Post, name="PostInResponse")

# Custom response model
class PostInResponseWithAuthor(BaseModel):
    id: int
    title: str
    content: str
    category: str
    author_username: Optional[str] = None  # Make it optional

    class Config:
        orm_mode = True
    
    def set_author_username(self, author_id: int):
        # Fetch the user and set the author's username
        user = User.get_or_none(id=author_id)
        if user:
            self.author_username = user.username


# Assuming UserOutResponse is defined as mentioned in the previous responses.
class PostCreateSchema(BaseModel):
    title: str
    content: str
    category: str
    author_id: int  # Include the author_id field

