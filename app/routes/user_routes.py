from fastapi import APIRouter, HTTPException
from app.models.user import *
import bcrypt
from app.schemas.post_models import *
from app.schemas.user_models import *
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.query_utils import Prefetch
import time
from tortoise.transactions import in_transaction
from app.models.comment import Comment

router = APIRouter()
@router.get("/{user_id}", response_model=user_pydantic_out, summary="Get User by ID", description="Retrieve user details by providing their ID.")
async def get_user(user_id: int):
    """
    Get User by ID
    Retrieve user details by providing their ID.
    
    :param user_id: ID of the user to retrieve.
    :return: User details.
    """
    user = await User.get_or_none(id=user_id)
    
    if user is None:
        error_msg = f"User with ID {user_id} not found"
        error_detail = {"error": error_msg}
        raise HTTPException(status_code=404, detail=error_detail)
    
    user_out_response = UserOutResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        join_date=user.join_date
    )
    return user_out_response


@router.post("/register", response_model=UserOutResponse, summary="Register User", description="Register a new user.")
async def register_user(user_data: UserInCreate):
    """
    Register User
    Register a new user.
    
    :param user_data: User data including username, email, and password.
    :return: Registered user details.
    """
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user using the data from the request
    new_user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password.decode('utf-8'),  # Store the hashed password in the database
    )

    user_out_response = UserOutResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        join_date=new_user.join_date
    )
    return user_out_response

@router.get("/{user_id}/posts_with_comments")
async def get_user_posts_with_comments(user_id: int):
    """
    Retrieve user's posts along with associated comments.

    This endpoint retrieves a user's posts along with their associated comments.
    The comments are fetched using Tortoise ORM's prefetch_related method
    to optimize database queries and improve performance.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing processing time and post-comment data.
    """

    start_time = time.time()

    user = await User.filter(id=user_id).prefetch_related(
        Prefetch('posts', queryset=Post.all().prefetch_related('comments__author'))
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posts_with_comments = []
    for post in user.posts:
        post_data = {
            'post_id': post.id,
            'title': post.title,
            'content': post.content,
            'comments': []
        }

        for comment in post.comments:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'email': comment.author.email
                }
            }
            post_data['comments'].append(comment_data)

        posts_with_comments.append(post_data)

    end_time = time.time()
    processing_time = end_time - start_time

    response = {
        'processing_time_in_ms': processing_time * 1000,
        'posts_with_comments': posts_with_comments
    }

    return response


## better with high number of comments
@router.get("/{user_id}/posts_with_comments_version_2")
async def get_user_posts_with_comments_version_2(user_id: int):
    """
    Retrieve user's posts along with associated comments (version 2).

    This endpoint retrieves a user's posts along with their associated comments
    using a bulk query strategy for improved performance when dealing with
    a larger number of comments. Comments are organized by post ID for efficient mapping.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary containing processing time and post-comment data.
    """
    
    start_time = time.time()

    user = await User.filter(id=user_id).first().prefetch_related(
        Prefetch('posts', queryset=Post.all().prefetch_related('comments__author'))
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Gather all post IDs for efficient query batching
    post_ids = [post.id for post in user.posts]

    # Fetch all comments for the user's posts in a single query
    comments = await Comment.filter(post_id__in=post_ids).prefetch_related('author')

    # Organize comments by post ID for easier mapping
    comments_by_post = {post_id: [] for post_id in post_ids}
    for comment in comments:
        comments_by_post[comment.post_id].append(comment)

    # Prepare response data
    posts_with_comments = []
    for post in user.posts:
        post_data = {
            'post_id': post.id,
            'title': post.title,
            'content': post.content,
            'comments': []
        }

        post_comments = comments_by_post.get(post.id, [])
        for comment in post_comments:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'email': comment.author.email
                }
            }
            post_data['comments'].append(comment_data)

        posts_with_comments.append(post_data)

    end_time = time.time()
    processing_time = end_time - start_time

    response = {
        'processing_time_in_ms': processing_time * 1000,
        'posts_with_comments': posts_with_comments
    }

    return response






