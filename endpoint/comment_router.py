from http import HTTPStatus
from fastapi import APIRouter
from services.comment_service import CommentService
from schema.comment import Comment

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

comment_service = CommentService()

@router.get("/", status_code=HTTPStatus.OK)
async def get_comments():
    return comment_service.get_comments()

@router.get("/{comment_id}", status_code=HTTPStatus.OK)
async def get_comment(comment_id: int):
    return comment_service.get_comment(comment_id)

@router.post("/", status_code=HTTPStatus.CREATED)
async def add_comment(comment: Comment):
    return comment_service.add_comment(comment)

@router.delete("/{comment_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_comment(comment_id: int):
    return comment_service.delete_comment(comment_id)

@router.put("/{comment_id}", status_code=HTTPStatus.OK)
async def update_comment(comment_id: int, comment: Comment):
    return comment_service.update_comment(comment_id, comment)

@router.get("/post/{post_id}", status_code=HTTPStatus.OK)
async def get_comments_by_post_id(post_id: int):
    return comment_service.get_comments_by_post_id(post_id)