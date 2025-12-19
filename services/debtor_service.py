
from database import get_connection
from schema.debtor import Debt, Debtor, RequestPayment

class DebtorService:

    def get_debtors(self):
        connect = get_connection()
        cursor = connect.cursor()
        try:
            cursor.execute("""
                SELECT 
                    d.debtor_id, 
                    d.full_name, 
                    d.phone_number,
                    COALESCE(SUM(CASE 
                        WHEN db.status = false THEN db.amount 
                        ELSE 0 
                    END), 0) AS total_debt
                FROM debtor d 
                LEFT JOIN debt db ON d.debtor_id = db.debtor_id 
                GROUP BY d.debtor_id 
                ORDER BY d.debtor_id
            """)
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
                    COALESCE(SUM(CASE 
                        WHEN db.status = false THEN db.amount 
                        ELSE 0 
                    END), 0) AS total_debt
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
                    debt_id,
                    date_time,
                    amount,
                    status
                FROM debt
                WHERE debtor_id = %s
                ORDER BY date_time DESC
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

    # def debt_repayment(self, debtor_id: int, amount: int):
    #     connect = get_connection()
    #     cursor = connect.cursor()
    #     debts = self.get_debt_by_debtor_id(debtor_id)
    #     copy_amount = amount
    #     for debt in debts:
    #         if debt["status"] == False:
    #             debt_id = debt["debt_id"]
    #             summa = self.get_payments_by_debt_id(debt_id)
    #             print("amount",debt["amount"], summa)
    #             while copy_amount > 0:
    #                 print(debt["status"])
    #                 if debt["status"] == True:
    #                     break
    #                 if copy_amount < debt["amount"] - summa:
    #                     cursor.execute("""
    #                     insert into payment_history (debt_id, amount)
    #                     values (%s, %s)
    #                     """, (debt_id, copy_amount))
    #                     copy_amount = 0
    #                 else:
    #                     # 120 000 - 100_000 = 20_000
    #                     # 30 000 - 20_000 = 10_000
    #                     cursor.execute("""
    #                     insert into payment_history (debt_id, amount)
    #                     values (%s, %s)
    #                     """, (debt_id, debt["amount"] - summa))

    #                     cursor.execute("""
    #                         UPDATE debt SET status = True WHERE debt_id = %s
    #                     """, (debt_id,))
    #                     copy_amount = copy_amount - (debt["amount"] - summa)

    #     connect.commit()
    #     cursor.close()
    #     connect.close()

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

    def debt_repayment(self, debtor_id: int, amount: int):
        connect = get_connection()
        cursor = connect.cursor()
        debts = self.get_debt_by_debtor_id(debtor_id)
        copy_amount = amount

        for i, debt in enumerate(debts):
            if debt["status"] == False:
                debt_id = debt["debt_id"]

                while copy_amount > 0:
                    # Refresh debt status from database
                    debt = self.get_debt_by_id(debt_id)  # Add this method if it doesn't exist

                    if debt["status"] == True:
                        break  # Move to next debt

                    # Get current payments for this debt
                    summa = self.get_payments_by_debt_id(debt_id)
                    remaining_debt = debt["amount"] - summa

                    print(f"Debt ID: {debt_id}, Remaining:  {remaining_debt}, Payment Amount: {copy_amount}")

                    if copy_amount >= remaining_debt:
                        # Pay off entire remaining debt
                        cursor.execute(
                            """
                            INSERT INTO payment_history (debt_id, amount)
                            VALUES (%s, %s)
                        """,
                            (debt_id, remaining_debt),
                        )

                        # Mark debt as paid
                        cursor.execute(
                            """
                            UPDATE debt SET status = True WHERE debt_id = %s
                        """,
                            (debt_id,),
                        )

                        copy_amount -= remaining_debt
                        print(f"Debt {debt_id} fully paid.  Remaining amount to distribute: {copy_amount}")
                        break  # Move to next debt
                    else:
                        # Partial payment
                        cursor.execute(
                            """
                            INSERT INTO payment_history (debt_id, amount)
                            VALUES (%s, %s)
                        """,
                            (debt_id, copy_amount),
                        )

                        copy_amount = 0
                        print(
                            f"Partial payment of {copy_amount} applied to debt {debt_id}"
                        )
                        break

        connect.commit()
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
                ORDER BY date_time
                """,
                (debt_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connect.close()


    def get_debts_history_by_debtor_id(self, debtor_id: int):
        connect = get_connection()
        cursor = connect.cursor()

        try:
            cursor.execute(
                """
                SELECT debt_id, amount, status, date_time
                FROM debt
                WHERE debtor_id = %s
                ORDER BY debt_id
                """,
                (debtor_id,),
            )
            debts = cursor.fetchall()

            result = []

            for debt in debts:
                payments = self.get_payment_history_by_debt_id(debt["debt_id"])

                total_paid = sum(p["amount"] for p in payments)

                result.append({
                    "debt_id": debt["debt_id"],
                    "date_time": debt["date_time"],
                    "amount": debt["amount"],
                    "status": debt["status"],
                    "total_paid": total_paid,
                    "remaining": debt["amount"] - total_paid,
                    "payments": payments,  
                })

            return result

        finally:
            cursor.close()
            connect.close()
