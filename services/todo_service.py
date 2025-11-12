from schema.todo import Todo
from fastapi import HTTPException


class TodoService:
    def __init__(self):
        self.todos = [
            {
                "user_id": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False
            },
            {
                "user_id": 3,
                "id": 2,
                "title": "quis ut nam facilis et officia qui",
                "completed": True
            }
        ]

    def get_todos(self):
        return self.todos
    
    def get_toto(self, todo_id):
        for todo in self.todos:
            if todo["id"] == todo_id:
                return todo
        return None
    
    def add_todo(self, todo: Todo):
        todo_data = todo.dict()
        todo_data["id"] = len(self.todos) + 1
        self.todos.append(todo_data)
        return todo_data

    def delete_todos(self, todo_id : int):
        for todo in self.todos:
            if todo["id"] == todo_id:
                self.todos.remove(todo)
                return todo
        return HTTPException(status_code=404, detail="Todo not found")
    
    def update_todo(self, todo_id: int, todo: Todo):
        todo = todo.dict()
        for t in self.todos:
            if t["id"] == todo_id:
                t.update(todo)
                return t
        return HTTPException(status_code=404, detail="Todo not found")
    
    def toggle_todo(self, todo_id: int):
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = not todo["completed"]
                return todo
        return HTTPException(status_code=404, detail="Todo not found")
    
    def get_todos_by_userId(self, user_id: int):
        new_todos = []
        for todo in self.todos:
            if todo["user_id"] == user_id:
                new_todos.append(todo)
        return new_todos