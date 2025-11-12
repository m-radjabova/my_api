from http import HTTPStatus
from fastapi import APIRouter
from schema.post import Post

from services.post_service import PostService

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

post_service = PostService()

@router.get("/", status_code=HTTPStatus.OK)
async def get_posts():
    return post_service.get_posts()

@router.post("/", status_code=HTTPStatus.CREATED)
async def add_post(post: Post):
    return post_service.add_post(post)

@router.get("/{post_id}", status_code=HTTPStatus.OK)
async def get_post(post_id: int):
    return post_service.get_post(post_id)

@router.delete("/{post_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_post(post_id: int):
    return post_service.delete_post(post_id)

@router.put("/{post_id}", status_code=HTTPStatus.OK)
async def update_post(post_id: int, req_post: Post):
    return post_service.update_post(post_id, req_post)

@router.get("/{user_id}", status_code=HTTPStatus.OK)
async def get_posts_by_userId(user_id: int):
    return post_service.get_posts_by_userId(user_id)