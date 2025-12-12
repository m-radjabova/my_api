from fastapi.responses import JSONResponse
from database import get_connection


class Comment :
    post_id: int
    name : str
    email: str
    body: str


class CommentService:

    def get_comments(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM comments")
            comments = cursor.fetchall()
            return comments
        finally:
            cursor.close()
            connect.close()

    def get_comment_by_post_id(self, post_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
            comments = cursor.fetchall()
            return comments
        finally:
            cursor.close()
            connect.close()

    def create_comment(self, comment: Comment):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "INSERT INTO comments (post_id, name, email, body) VALUES (%s, %s, %s, %s)",
                (comment.post_id, comment.name, comment.email, comment.body)
            )
            connect.commit()
            return comment
        finally:
            cursor.close()
            connect.close()

    def delete_comment(self, comment_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("DELETE FROM comments WHERE comment_id = %s", (comment_id,))
            connect.commit()
            return JSONResponse(status_code=204, content={"message": "Comment deleted successfully"})
        finally:
            cursor.close()
            connect.close()

    
        