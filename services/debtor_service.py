from pydantic import BaseModel

from database import get_connection


class Debtor(BaseModel):
    full_name: str
    phone_number: str


class Debt(BaseModel):
    amount: int
    status: bool = False

class RequestPayment(BaseModel):
    amount: int


class DebtorService:

    def get_debtors(self):
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
                GROUP BY d.debtor_id
                ORDER BY d.debtor_id
                """
            )
            debtors = cursor.fetchall()
            return debtors
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
                (debtor_id,)
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
                    debt_id,
                    date_time,
                    amount,
                    status
                FROM debt
                WHERE debtor_id = %s
                ORDER BY date_time DESC
                """,
                (debtor_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connect.close()


    def debt_repayment (self, debtor_id: int, amount: int):
        connect = get_connection()
        cursor = connect.cursor()

        debts = self.get_debt_by_debtor_id(debtor_id)
        print("debtor_id", debtor_id)
        copy_amount = amount
        for debt in debts:
            if debt['status'] == False:
                debt_id = debt['debt_id']
                print("debt amount", debt["amount"])
                while copy_amount > debt['amount']:
                    copy_amount -= debt['amount']
                    debt = Debt(amount=debt['amount'], status=False)
                    connect.commit()
               
                return {"message": "Debt repayment successful"}