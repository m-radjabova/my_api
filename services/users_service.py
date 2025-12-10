from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from database import get_connection


class User(BaseModel):
    email: str = Field(..., max_length=256)
    phone_number: str


class UsersService:

    def get_users(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Users not found")

        finally:
            cursor.close()
            connect.close()

    def create_user(self, user: User):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, phone_number) VALUES (%s, %s)",
                (user.email, user.phone_number)
            )
            connect.commit()

            return user

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="User already exists")

        finally:
            cursor.close()
            connect.close()

    def delete_user(self, user_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connect.commit()
            return JSONResponse(status_code=204, content={"message": "User deleted successfully"})

        except Exception as e: 
            print(str(e)) 
            raise HTTPException(status_code=404, detail="User not found")
        finally:
            cursor.close()
            connect.close()

    def update_user(self, user_id: int, user: User):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "UPDATE users SET email=%s, phone_number=%s WHERE id=%s",
                (user.email, user.phone_number, user_id)
            )
            connect.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "id": user_id,
                "email": user.email,
                "phone_number": user.phone_number
            }

        finally:
            cursor.close()
            connect.close()
