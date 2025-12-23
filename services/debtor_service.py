
from database import get_connection
from schema.debtor import Debt, Debtor, RequestPayment

class DebtorService:

    def get_debtors(self, name: str = None, page: int = 1, limit: int = 5):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            page = max(1, page)  
            limit = max(1, min(limit, 100))  
            offset = (page - 1) * limit

            conditions = []
            filter_values = []

            if name:
                conditions.append("d.full_name ILIKE %s")
                filter_values.append(f"%{name}%")

            where_clause = ""
            if conditions:
                where_clause = " WHERE " + " AND ".join(conditions)

            count_query = "SELECT COUNT(*) AS count FROM debtor d" + where_clause
            cursor.execute(count_query, filter_values)
            total = cursor.fetchone()['count']

            data_query = """
                SELECT 
                    d.debtor_id, 
                    d.full_name, 
                    d.phone_number,
                    COALESCE(SUM(
                        CASE 
                            WHEN db.status = false THEN db.amount 
                            ELSE 0 
                        END
                    ), 0) AS total_debt
                FROM debtor d 
                LEFT JOIN debt db ON d.debtor_id = db.debtor_id
            """ + where_clause +  """
                GROUP BY d.debtor_id, d.full_name, d.phone_number
                LIMIT %s OFFSET %s
            """

            data_values = filter_values + [limit, offset]
            cursor.execute(data_query, data_values)
            cars = cursor.fetchall()

            return {
                "data": cars,
                "total": total,
                "page": page,
                "limit": limit,
            }

        finally:
            cursor.close()
            connect.close()


    def get_debtor_by_id(self, debtor_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                SELECT 
                    d.debtor_id,
                    d.full_name,
                    d.phone_number,
                    COALESCE(SUM(db.amount), 0) AS total_debt
                FROM debtor d
                LEFT JOIN debt db ON d.debtor_id = db.debtor_id
                WHERE d.debtor_id = %s
                GROUP BY d.debtor_id
                """,
                (debtor_id,),
            )
            debtor = cursor.fetchone()
            return debtor
        finally:
            cursor.close()
            connect.close()

    def create_debtor(self, debtor: Debtor):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                "INSERT INTO debtor (full_name, phone_number) VALUES (%s, %s) RETURNING debtor_id",
                (debtor.full_name, debtor.phone_number),
            )
            debtor_id = cursor.fetchone()["debtor_id"]
            connect.commit()
            return debtor_id
        finally:
            cursor.close()
            connect.close()

    def add_debt_to_debtor(self, debtor_id: int, debt: Debt):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO debt (debtor_id, amount, status)
                VALUES (%s, %s, %s)
                RETURNING debt_id
                """,
                (debtor_id, debt.amount, debt.status),
            )
            debt_id = cursor.fetchone()["debt_id"]
            connect.commit()
            return {"debt_id": debt_id}
        finally:
            cursor.close()
            connect.close()

    def get_debt_by_debtor_id(self, debtor_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                SELECT 
                    db.debt_id,
                    db.date_time,
                    db.amount,
                    db.status,
                    GREATEST(
                        db.amount - COALESCE(SUM(p.amount), 0),
                        0
                    ) AS remaining
                    
                FROM debt db
                LEFT JOIN payment_history p 
                    ON db.debt_id = p.debt_id
                WHERE db.debtor_id = %s
                GROUP BY db.debt_id
                ORDER BY db.date_time DESC
                """,
                (debtor_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connect.close()

    def get_payments_by_debt_id(self, debt_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                SELECT 
                    COALESCE(SUM(amount), 0) AS summa
                FROM payment_history
                WHERE debt_id = %s
                """,
                (debt_id,),
            )
            result = cursor.fetchone()
            return result["summa"]
        finally:
            cursor.close()
            connect.close()

    def get_debt_by_id(self, debt_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        cursor.execute(
            """
            SELECT debt_id, debtor_id, amount, status FROM debt WHERE debt_id = %s
        """,
            (debt_id,),
        )
        result = cursor.fetchone()
        cursor.close()
        connect.close()

        if result:
            return result
        return None

    def repay_single_debt(self, debt_id: int, amount: int):
        connect = get_connection()
        cursor = connect.cursor()
        debt = self.get_debt_by_id(debt_id)
        if not debt or debt["status"] == True:
            cursor.close()
            connect.close()
            return  

        summa = self.get_payments_by_debt_id(debt_id)
        remaining_debt = debt["amount"] - summa

        if amount >= remaining_debt:
            cursor.execute(
                """
                INSERT INTO payment_history (debt_id, amount)
                VALUES (%s, %s)
            """,
                (debt_id, remaining_debt),
            )

            cursor.execute(
                """
                UPDATE debt SET status = True WHERE debt_id = %s
            """,
                (debt_id,),
            )
        else:
            cursor.execute(
                """
                INSERT INTO payment_history (debt_id, amount)
                VALUES (%s, %s)
            """,
                (debt_id, amount),
            )

        connect.commit()
        cursor.close()
        connect.close()

    def debt_repayment(self, debtor_id: int, amount: int):
        connect = get_connection()
        cursor = connect.cursor()
        
        try:
            cursor.execute(
                """
                SELECT 
                    db.debt_id,
                    db.amount,
                    db.status,
                    COALESCE(SUM(p.amount), 0) AS paid_amount,
                    db.amount - COALESCE(SUM(p.amount), 0) AS remaining
                FROM debt db
                LEFT JOIN payment_history p ON db.debt_id = p.debt_id
                WHERE db.debtor_id = %s AND db.status = False
                GROUP BY db.debt_id, db.amount, db.status
                ORDER BY db.date_time ASC
                """,
                (debtor_id,)
            )
            debts = cursor.fetchall()
            
            if not debts:
                cursor.close()
                connect.close()
                return {
                    "success": False, 
                    "message": "To'lanmagan qarz topilmadi",
                    "remaining_amount": amount
                }
            
            remaining_amount = amount
            processed_debts = []
            
            for debt in debts:
                if remaining_amount <= 0:
                    break
                
                debt_id = debt["debt_id"]
                debt_remaining = debt["remaining"]
                
                if remaining_amount >= debt_remaining:
                    cursor.execute(
                        """
                        INSERT INTO payment_history (debt_id, amount)
                        VALUES (%s, %s)
                        """,
                        (debt_id, debt_remaining)
                    )
                    
                    cursor.execute(
                        """
                        UPDATE debt SET status = True WHERE debt_id = %s
                        """,
                        (debt_id,)
                    )
                    
                    remaining_amount -= debt_remaining
                    processed_debts.append({
                        "debt_id": debt_id,
                        "paid": debt_remaining,
                        "status": "fully_paid"
                    })
                else:
                    cursor.execute(
                        """
                        INSERT INTO payment_history (debt_id, amount)
                        VALUES (%s, %s)
                        """,
                        (debt_id, remaining_amount)
                    )
                    
                    processed_debts.append({
                        "debt_id": debt_id,
                        "paid": remaining_amount,
                        "status": "partially_paid"
                    })
                    
                    remaining_amount = 0
            
            connect.commit()
            
            return {
                "success": True,
                "message": "To'lov muvaffaqiyatli amalga oshirildi",
                "total_paid": amount,
                "remaining_amount": remaining_amount,  
                "processed_debts": processed_debts
            }
            
        except Exception as e:
            connect.rollback()
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            connect.close()

    def get_debts_history_by_debtor_id(self, debtor_id: int):
        connect = get_connection()
        cursor = connect.cursor()

        try:
            cursor. execute(
                """
                SELECT debt_id, amount, status, date_time
                FROM debt
                WHERE debtor_id = %s
                ORDER BY date_time DESC
                """,
                (debtor_id,),
            )
            debts = cursor.fetchall()

            result = []

            for debt in debts: 
                payments = self.get_payment_history_by_debt_id(debt["debt_id"])

                total_paid = sum(p["amount"] for p in payments)
                remaining = debt["amount"] - total_paid

                result.append({
                    "debt_id":  debt["debt_id"],
                    "date_time": debt["date_time"],
                    "amount":  debt["amount"],
                    "status": debt["status"],
                    "total_paid": total_paid,
                    "remaining": remaining,
                    "payments": payments,  
                })

            return result

        finally:
            cursor.close()
            connect.close()


    def get_payment_history_by_debt_id(self, debt_id: int):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute(
                """
                SELECT 
                    payment_history_id,
                    date_time,
                    amount
                FROM payment_history
                WHERE debt_id = %s
                ORDER BY date_time DESC
                """,
                (debt_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connect.close()