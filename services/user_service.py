from typing import List
from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.users = [
            {
                "id": 1,
                "username": "Muslima Radjabova",
                "email": "muslima@gmail.com",
            },
            {
                "id": 2,
                "username": "Daler Ismatov",
                "email": "ismatov@gmail.com",
            },
        ]

    def get_users(self):
        return self.users
    
    def get_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return HTTPException(status_code=404, detail="User not found")