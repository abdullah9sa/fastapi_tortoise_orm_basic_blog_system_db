from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    user_id: int
    post_id: int
    pass

class Comment(CommentBase):
    id: int
    class Config:
        orm_mode = True
