from fastapi import HTTPException
from schema.comment import Comment

class CommentService:
    def __init__(self):
        self.comments = [
            {
                "postId": 1,
                "id": 1,
                "name": "id labore ex et quam laborum",
                "email": "Eliseo@gardner.biz",
                "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium",
            }
        ]

    def get_comments(self):
        return self.comments
    

    def get_comment(self, comment_id):
        for comment in self.comments:
            if comment["id"] == comment_id:
                return comment
        return HTTPException(status_code=404, detail="Comment not found")
    

    def add_comment(self, comment: Comment):
        print(f"Backendga kelgan ma'lumot: {comment.dict()}")
        comment_data = comment.dict()
        comment_data["id"] = len(self.comments) + 1
        self.comments.append(comment_data)
        print(f"Qo'shilgandan keyin comments: {self.comments}")
        return comment_data

    def delete_comment(self, comment_id):
        for comment in self.comments:
            if comment["id"] == comment_id:
                self.comments.remove(comment)
                return comment
        return HTTPException(status_code=404, detail="Comment not found")
    

    def update_comment(self, comment_id, comment: Comment):
        comment = comment.dict()
        for c in self.comments:
            if c["id"] == comment_id:
                c.update(comment)
                return c
        return HTTPException(status_code=404, detail="Comment not found")
    
    def get_comments_by_post_id(self, post_id):
        new_com = []
        for comment in self.comments:
            if comment["postId"] == post_id:
                new_com.append(comment)
        return new_com
