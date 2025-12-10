from fastapi import APIRouter, HTTPException, status
from services.posts_service import Comment, Post, PostService

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

post_service = PostService()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts():
    return post_service.get_posts()

@router.get("/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    return post_service.get_post_by_id(post_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post_service.create_post(post)

@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int):
    return post_service.delete_post(post_id)

@router.put("/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: Post):
    return post_service.update_post(post_id, post)
