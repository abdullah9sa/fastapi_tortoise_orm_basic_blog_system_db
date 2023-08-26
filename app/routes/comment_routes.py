from fastapi import APIRouter, HTTPException
from app.models.post import Post
from app.schemas.comment_models import CommentCreate
from app.models.comment import Comment

router = APIRouter()

@router.post("/create/")
async def create_comment(comment: CommentCreate):
    post = await Post.filter(id=comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = await Comment.create(content=comment.content, post=post, author_id=comment.user_id)

    return new_comment
