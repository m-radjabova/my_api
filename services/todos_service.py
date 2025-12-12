from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import get_connection


class Todo(BaseModel):
    title : str
    completed : bool
    user_id : int

class TodosService:
    def get_todos(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM todos")
            todos = cursor.fetchall()
            return todos
        finally:
            cursor.close()
            connect.close()

    def create_todo(self, todo: Todo):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("INSERT INTO todos (title, completed, user_id) VALUES (%s, %s, %s)", 
                (todo.title, todo.completed, todo.user_id))
            connect.commit()
            return todo
        finally:
            cursor.close()
            connect.close()
    
    def delete_todo(self, todo_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("DELETE FROM todos WHERE todo_id = %s", (todo_id,))
            connect.commit()
            return JSONResponse(status_code=204, content={"message": "Todo deleted successfully"})
        finally:
            cursor.close()
            connect.close()

    def update_todo(self, todo_id: int, todo: Todo):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("UPDATE todos SET title=%s, completed=%s, user_id=%s WHERE id=%s", (todo.title, todo.completed, todo.user_id, todo_id))
            connect.commit()
            return todo
        finally:
            cursor.close()
            connect.close()
            
    def get_todo_by_user_id(self, user_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM todos WHERE user_id = %s", (user_id,))
            todos = cursor.fetchall()
            return todos
        finally:
            cursor.close()
            connect.close()

    def toogle_todo_completed(self, todo_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("""
                UPDATE todos 
                SET completed = NOT completed 
                WHERE todo_id = %s
                RETURNING todo_id, completed;
            """, (todo_id,))
            
            updated = cursor.fetchone()
            connect.commit()

            if not updated:
                raise HTTPException(status_code=404, detail="Todo not found")

            # updated — tuple (todo_id, completed)
            todo_id_value, completed_value = updated

            return {
                "todo_id": todo_id_value,
                "completed": completed_value
            }

        finally:
            cursor.close()
            connect.close()

