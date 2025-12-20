from fastapi import APIRouter

from services.debtor_service import Debt, Debtor, DebtorService, RequestPayment


router = APIRouter(
    prefix="/debtor",
    tags=["debtor"],
)

debtor_service = DebtorService()


@router.get("/", status_code=200)
async def get_debtors(name: str = None, page: int = 1, limit: int = 5):
    return debtor_service.get_debtors(name, page, limit)

@router.get("/{debtor_id}", status_code=200)
async def get_debtor(debtor_id: int):
    return debtor_service.get_debtor_by_id(debtor_id)

@router.get("/{debtor_id}/debts")
async def get_debts(debtor_id: int):
    return debtor_service.get_debt_by_debtor_id(debtor_id)


@router.post("/", status_code=201)
async def create_debtor(debtor: Debtor):
    return debtor_service.create_debtor(debtor)


@router.post("/{debtor_id}/debt", status_code=201)
async def add_debt_to_debtor(debtor_id: int, debt: Debt):
    return debtor_service.add_debt_to_debtor(debtor_id, debt)


@router.post("/{debtor_id}/repayment", status_code=201)
async def debt_repayment(debtor_id: int, payload: RequestPayment):
    return debtor_service.debt_repayment(
        debtor_id,
        payload.amount
    )

@router.get("/{debtor_id}/debts-history", status_code=200)
async def debts_history_by_debtor_id(debtor_id: int):
    return debtor_service.get_debts_history_by_debtor_id(debtor_id)
