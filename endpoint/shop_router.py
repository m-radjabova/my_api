from http.client import HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from services.debtor_service import DebtorService
from services.shop_service import ShopService


shop_router = APIRouter(
    prefix="/shop",
    tags=["shop"],
)

shop_service = ShopService()
debtor_service = DebtorService()


class ShopCreate(BaseModel):
    shop_name: str
    owner_name: str
    phone_number: str
    address: str


class ShopUpdate(BaseModel):
    shop_name: str
    owner_name: str
    phone_number: str
    address: str

@shop_router.post("/", status_code=201)
async def create_shop(shop: ShopCreate):
    result = shop_service.create_shop(
        shop.shop_name,
        shop.owner_name,
        shop.phone_number,
        shop.address
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result


@shop_router.get("/", status_code=200)
async def get_all_shops():
    shops = shop_service.get_all_shops()
    return {"shops": shops, "total": len(shops)}


@shop_router.get("/{shop_id}", status_code=200)
async def get_shop(shop_id: int):
    shop = shop_service.get_shop_by_id(shop_id)
    
    if not shop:
        raise HTTPException(status_code=404, detail="Do'kon topilmadi")
    
    return shop

@shop_router.get("/{shop_id}/statistics", status_code=200)
async def get_shop_statistics(shop_id: int):
    shop = shop_service.get_shop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Do'kon topilmadi")
    
    stats = debtor_service.get_shop_statistics(shop_id)
    
    return {
        "shop_id": shop_id,
        "shop_name": shop["shop_name"],
        "statistics": stats
    }

@shop_router.put("/{shop_id}", status_code=200)
async def update_shop(shop_id: int, shop: ShopUpdate):
    result = shop_service.update_shop(shop_id, shop.shop_name, shop.owner_name, shop.phone_number, shop.address)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result
from typing import Optional

@shop_router.post("/login", status_code=200)
async def login_shop(shop_name: str):
    shop = shop_service.get_shop_by_name(shop_name)
    
    if not shop:
        raise HTTPException(status_code=401, detail="Do'kon nomi noto'g'ri")
    
    return {
        "success": True,
        "message": "Login muvaffaqiyatli",
        "shop": shop
    }

@shop_router.get("/search/", status_code=200)
async def search_shops(name: Optional[str] = None):
    if not name:
        shops = shop_service.get_all_shops()
    else:
        shops = shop_service.search_shops_by_name(name)
    
    return {"shops": shops, "total": len(shops)}