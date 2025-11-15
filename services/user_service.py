from typing import List
from fastapi import HTTPException


class UserService:
    def __init__(self):
        self.users = [
            {
                "id": 1,
                "username": "John Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "Turon Street",
                    "city": "Bukhara",
                },
            },
            {
                "id": 2,
                "username": "Jane Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Bukhara",
                },
            },
            {
                "id": 3,
                "username": "Joke Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Samarkand",
                },
            },
            {
                "id": 4,
                "username": "Mary Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Navoiy",
                },
            },
            {
                "id": 5,
                "username": "Mark Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Navoiy",
                },
            },
            {
                "id": 6,
                "username": "Josef Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Xorazm",
                },
            },
            {
                "id": 7,
                "username": "Mia Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Samarkand",
                },
            },
            {
                "id": 8,
                "username": "Yuna Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Bukhara",
                },
            },
            {
                "id": 9,
                "username": "Yuki Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Bukhara",
                },
            },
            {
                "id": 10,
                "username": "Yui Doe",
                "email": "9yX5k@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "Samarkand",
                },
            },
        ]

    def get_users(self, cities: List[str] = None, page=1, limit=10):
        if cities:
            filtered = self.__get_users_by_cities(cities)
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
    
    def get_cities(self):
        cities = set()
        for user in self.users:
            cities.add(user["address"]["city"])
        return list(cities)

    def __get_users_by_cities(self, cities):
        if not cities:
            return self.users

        cities = [c.lower() for c in cities]

        return [
            user for user in self.users
            if user["address"]["city"].lower() in cities
        ]


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