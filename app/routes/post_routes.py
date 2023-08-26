from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.post import *
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[PostInResponseWithAuthor], summary="Get Posts", description="Retrieve a list of posts.")
async def get_posts(
    author: str = Query(None, description="Filter posts by author username."),
    category: str = Query(None, description="Filter posts by category.")
):
    """
    Get Posts
    Retrieve a list of posts. You can filter posts by author username or category.

    :param author: Filter posts by author username.
    :param category: Filter posts by category.
    :return: List of posts with author details.
    """
    query = Post.filter()

    if author:
        query = query.filter(author__username=author)
    if category:
        query = query.filter(category=category)

    posts = await query

    posts_with_author = []

    for post in posts:
        author_username = await User.get_or_none(id=post.author_id)
        if author_username:
            post_with_author = PostInResponseWithAuthor(
                id=post.id,
                title=post.title,
                content=post.content,
                category=post.category,
                author_id=post.author_id,
                author_username=author_username.username
            )
            posts_with_author.append(post_with_author)

    return posts_with_author

@router.post("/", response_model=PostInResponse, summary="Create Post", description="Create a new post.")
async def create_post(
    post_data: PostCreateSchema
):
    """
    Create Post
    Create a new post.

    :param post_data: Data for creating the post.
    :return: Newly created post.
    """
    # Validate if the author user exists
    author = await User.get_or_none(id=post_data.author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")


    # Create a new post
    new_post = await Post.create(
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        author=author,
    )

    return new_post
