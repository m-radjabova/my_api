from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import get_connection

class Post(BaseModel):
    title: str
    body : str
    user_id: int

class Comment(BaseModel):
    post_id: int
    name : str
    email: str
    body: str

class PostService:

    def get_posts(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM posts")
            return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Posts not found")

        finally:
            cursor.close()
            connect.close()

    def create_post(self, post: Post):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            print(post)
            cursor.execute(
                "INSERT INTO posts (title, body, user_id) VALUES (%s, %s, %s)",
                (post.title, post.body, post.user_id)
            )
            connect.commit()
            return post
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Post already exists")
        finally:
            cursor.close()
            connect.close()

    
    def delete_post(self, post_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            connect.commit()
            return JSONResponse(status_code=204, content={"message": "Post deleted successfully"})

        except Exception as e: 
            print(str(e)) 
            raise HTTPException(status_code=404, detail="Post not found")
        finally:
            cursor.close()
            connect.close()

    def update_post(self, post_id: int, post: Post):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "UPDATE posts SET title=%s, body=%s, user_id=%s WHERE id=%s",
                (post.title, post.body, post.user_id, post_id)
            )
            connect.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Post not found")

            return {
                "id": post_id,
                "title": post.title,
                "body": post.body,
                "user_id": post.user_id
            }

        finally:
            cursor.close()
            connect.close()
