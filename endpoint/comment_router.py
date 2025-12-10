
from fastapi import APIRouter

from services.comment_service import CommentService
from services.posts_service import Comment


router = APIRouter(
    prefix="/comments",
    tags=["comment"],
)

comment_service = CommentService()

@router.get("/", status_code=200)
async def get_comments():
    return comment_service.get_comments()


@router.get("/post/{post_id}", status_code=200)
async def get_comments_by_post_id(post_id: int):
    return comment_service.get_comment_by_post_id(post_id)


@router.post("/", status_code=201)
async def create_comment(comment: Comment):
    return comment_service.create_comment(comment)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int):
    return comment_service.delete_comment(comment_id)