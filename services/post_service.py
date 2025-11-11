from pydantic import BaseModel, Field
from typing import Optional

from schema.post import Post


class PostService:
    def __init__(self):
        self.posts = [
            {
                "id": 1,
                "title": "First Post",
                "body": "This is the first post",
                "user_id": 1
            },
            {
                "id": 2,
                "title": "Second Post",
                "body": "This is the second post",
                "user_id": 1
            }
        ]

    def get_posts(self):
        return self.posts
    
    def get_post(self, post_id):
        for post in self.posts:
            if post["id"] == post_id:
                return post
        return None
    
    def add_post(self, post: Post):
        post_data = post.dict()
        post_data["id"] = len(self.posts) + 1
        self.posts.append(post_data)
        return post_data

    def delete_post(self, post_id: int):
        for post in self.posts:
            if post["id"] == post_id:
                self.posts.remove(post)
                return post
        return None

    def update_post(self, post_id: int, post: Post):
        post = post.dict()
        for p in self.posts:
            if p["id"] == post_id:
                p.update(post)
                return p
        return None
