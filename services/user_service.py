from typing import List
from fastapi import HTTPException

from schema.user import RequestUser


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
    
    def create_user(self, user_data : RequestUser):
        user_dict = user_data.model_dump()
        user_dict["id"] = len(self.users) + 1
        self.users.append(user_dict)
        return user_dict
    
    def delete_user(self, user_id):
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                del self.users[i]
                return True
        return False

    def update_user(self, user_id, user_data: RequestUser):
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                updated = user_data.model_dump()
                updated["id"] = user_id
                self.users[i] = updated
                return updated
        return None