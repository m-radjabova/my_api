from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.users = [
            {
                "id": 1,
                "username": "John Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 2,
                "username": "Jane Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 3,
                "username": "Joke Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 4,
                "username": "Mary Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 5,
                "username": "Mark Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 6,
                "username": "Josef Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 7,
                "username": "Mia Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 8,
                "username": "Yuna Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 9,
                "username": "Yuki Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
            {
                "id": 10,
                "username": "Yui Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                },
            },
        ]

    def get_users(self, username=None, page=1, limit=4):
        if username:
            filtered = self.__get_users_by_username(username)
        else:
            filtered = self.users

        total = len(filtered)

        start = (page - 1) * limit
        end = start + limit

        data = filtered[start:end]

        return {
            "data": data,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }


    def __get_users_by_username(self, username):
        arr = []
        for user in self.users:
            if username.lower() in user["username"].lower():
                arr.append(user)
        return arr

    def get_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return HTTPException(status_code=404, detail="User not found")

    def create_user(self, user):
        user = user.dict()
        user["id"] = len(self.users) + 1
        self.users.append(user)
        return user

    def delete_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                self.users.remove(user)
                return user
        return HTTPException(status_code=404, detail="User not found")

    def update_user(self, user_id, user):
        user = user.dict()
        for u in self.users:
            if u["id"] == user_id:
                u.update(user)
                return u
        return HTTPException(status_code=404, detail="User not found")

    def increment_age(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                user["age"] += 1
                return user
        return HTTPException(status_code=404, detail="User not found")

    def decrement_age(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                user["age"] -= 1
                return user
        return HTTPException(status_code=404, detail="User not found")
