from datetime import date
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from database import get_connection


class Details (BaseModel):
    name: str

class Car (BaseModel):
    model : str
    color : str
    year_purchased: int
    details : List[Details]


class CarService:
    def __init__(self):
        self.connect = get_connection()
        self.cursor = self.connect.cursor()

    def get_cars(
        self,
        model: str = None,
        color: str = None,
        year: int = None,
        page: int = 1,
        limit: int = 10
    ):
        connect = get_connection()
        cursor = connect.cursor()

        try:
            limit = max(1, min(limit, 100))  
            offset = (page - 1) * limit
            

            conditions = []
            filter_values = []

            if model:
                conditions.append("c.model ILIKE %s")
                filter_values.append(f"%{model}%")
            if color:
                conditions.append("c.color ILIKE %s")
                filter_values.append(f"%{color}%")
            if year:
                conditions.append("c.year_purchased = %s")
                filter_values.append(year)

            where_clause = ""
            if conditions:
                where_clause = " WHERE " + " AND ".join(conditions)

            count_query = "SELECT COUNT(*) AS count FROM car c" + where_clause
            cursor.execute(count_query, filter_values)
            total = cursor.fetchone()['count']

            data_query = f"""
                SELECT 
                    c.car_id,
                    c.model,
                    c.color,
                    c.year_purchased,
                    COALESCE(
                        json_agg(
                            json_build_object(
                                'id', d.detail_id,
                                'name', d.name
                            )
                        ) FILTER (WHERE d.detail_id IS NOT NULL),
                        '[]'
                    ) AS details
                FROM car c
                LEFT JOIN details d ON c.car_id = d.car_id
                {where_clause}
                GROUP BY c.car_id
                ORDER BY c.car_id
                LIMIT %s OFFSET %s
            """
            
            data_values = filter_values + [limit, offset]
            cursor.execute(data_query, data_values)
            cars = cursor.fetchall()

            return {
                "data": cars,
                "total": total,
                "page": page,
                "limit": limit
            }

        finally:
            cursor.close()
            connect.close()

    def create_car(self, car: Car):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "INSERT INTO car (model, color, year_purchased) VALUES (%s, %s, %s) RETURNING car_id",
                (car.model, car.color, car.year_purchased),
            )
            car_id = cursor.fetchone()['car_id']
            for detail in car.details:
                cursor.execute(
                    "INSERT INTO details (car_id, name) VALUES (%s, %s)",
                    (car_id, detail.name)
                )
            connect.commit()
            return car
        finally:
            cursor.close()
            connect.close()

    def get_car_by_id(self, car_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM car WHERE car_id = %s", (car_id,))
            car = cursor.fetchone()
            return car
        finally:
            cursor.close()
            connect.close()

    def update_car(self, car_id: int, car: Car):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                UPDATE car 
                SET model = %s, color = %s, year_purchased = %s 
                WHERE car_id = %s
                RETURNING car_id
                """,
                (car.model, car.color, car.year_purchased, car_id),
            )
            car_id = cursor.fetchone()['car_id']

            cursor.execute(
                "DELETE FROM details WHERE car_id = %s",
                (car_id,)
            )

            for detail in car.details:
                cursor.execute(
                    "INSERT INTO details (car_id, name) VALUES (%s, %s)",
                    (car_id, detail.name)
                )

            connect.commit()
            return car

        finally:
            cursor.close()
            connect.close()


    def delete_car(self, car_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("DELETE FROM car WHERE car_id = %s", (car_id,))
            connect.commit()
            return JSONResponse(status_code=204, content={"message": "Car deleted successfully"})
        finally:
            cursor.close()
            connect.close()

    def get_color_from_cars(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT DISTINCT color FROM car")
            colors = cursor.fetchall()
            return colors
        finally:
            cursor.close()
            connect.close()

    