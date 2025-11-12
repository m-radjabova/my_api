import json
from fastapi import HTTPException, requests
from schema.post import Post


class PostService:
    def __init__(self):
        self.posts = [
            {
                "user_id": 1,
                "id": 1,
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
            },
            {
              "user_id": 1,
              "id": 2,
              "title": "qui est esse",
              "body": "woww woowwbfeknwbvjmdc vjhfknfbvdjhk"
            }
        ]

    def get_posts(self):
        return self.posts
    
    def get_post(self, post_id):
        for post in self.posts:
            if post["id"] == post_id:
                return post
        return HTTPException(status_code=404, detail="Post not found")
    
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
        return HTTPException(status_code=404, detail="Post not found")

    def update_post(self, post_id: int, post: Post):
        post = post.dict()
        for p in self.posts:
            if p["id"] == post_id:
                p.update(post)
                return p
        return HTTPException(status_code=404, detail="Post not found")
    
    def get_posts_by_userId(self, user_id: int):
        news_posts = []
        for post in self.posts:
            if post["user_id"] == user_id:
                news_posts.append(post)
        return news_posts