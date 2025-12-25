from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.debtor_service import Debt, Debtor, DebtorService, RequestPayment

router = APIRouter(
    prefix="/debtor",
    tags=["debtor"],
)

debtor_service = DebtorService()

class RepaymentRequest(BaseModel):
    amount: int

@router.get("/", status_code=200)
async def get_debtors(shop_id: int, name: str = None, page: int = 1, limit: int = 5):
    return debtor_service.get_debtors(shop_id, name, page, limit)

@router.get("/{debtor_id}", status_code=200)
async def get_debtor(debtor_id: int, shop_id: int):
    result = debtor_service.get_debtor_by_id(debtor_id, shop_id)
    if not result:
        raise HTTPException(status_code=404, detail="Debtor not found")
    return result

@router.get("/{debtor_id}/debts", status_code=200)
async def get_debts(debtor_id: int, shop_id: int):
    # Shop_id tekshiruvi qo'shildi
    result = debtor_service.get_debt_by_debtor_id(debtor_id, shop_id)
    return result

@router.post("/", status_code=201)
async def create_debtor(debtor: Debtor):
    return {"debtor_id": debtor_service.create_debtor(debtor.shop_id, debtor)}

@router.post("/{debtor_id}/debt", status_code=201)
async def add_debt_to_debtor(debtor_id: int, debt: Debt, shop_id: int):
    result = debtor_service.add_debt_to_debtor(debtor_id, shop_id, debt)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.post("/debt/{debt_id}/repayment", status_code=200)
async def repay_single_debt(debt_id: int, payload: RepaymentRequest, shop_id: int):
    result = debtor_service.repay_single_debt(debt_id, payload.amount, shop_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=400, 
            detail=result["message"],
            headers={"remaining_amount": str(result.get("remaining_amount", 0))}
        )
    
    return {
        "success": True, 
        "message": result["message"],
        "debt_id": debt_id,
        "amount_paid": result["paid"],
        "status": result["status"]
    }

@router.post("/{debtor_id}/repayment", status_code=201)
async def debt_repayment(debtor_id: int, payload: RequestPayment, shop_id: int):
    result = debtor_service.debt_repayment(debtor_id, payload.amount, shop_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/{debtor_id}/debts-history", status_code=200)
async def debts_history_by_debtor_id(debtor_id: int, shop_id: int):
    result = debtor_service.get_debts_history_by_debtor_id(debtor_id, shop_id)
    return result