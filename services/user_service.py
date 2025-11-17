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

    # def create_user(self, user):
    #     user = user.dict()
    #     user["id"] = len(self.users) + 1
    #     self.users.append(user)
    #     return user

    # def delete_user(self, user_id):
    #     for user in self.users:
    #         if user["id"] == user_id:
    #             self.users.remove(user)
    #             return user
    #     return HTTPException(status_code=404, detail="User not found")

    # def update_user(self, user_id, user):
    #     user = user.dict()
    #     for u in self.users:
    #         if u["id"] == user_id:
    #             u.update(user)
    #             return u
    #     return HTTPException(status_code=404, detail="User not found")