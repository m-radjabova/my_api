from fastapi import APIRouter

from services.cars_service import Car, CarService


router = APIRouter(
    prefix="/cars",
    tags=["cars"],
)

car_service = CarService()


@router.get("/", status_code=200)
async def get_cars(model: str = None, color: str = None, year: int = None, page: int = 1, limit: int = 10):
    return car_service.get_cars( model, color, year, page, limit)

@router.get("/colors", status_code=200)
async def get_colors_from_cars():
    return car_service.get_color_from_cars()


@router.post("/", status_code=201)
async def create_car(car: Car):
    return car_service.create_car(car)


@router.get("/{car_id}", status_code=200)
async def get_car(car_id: int):
    return car_service.get_car_by_id(car_id)


@router.put("/{car_id}", status_code=200)
async def update_car(car_id: int, car: Car):
    return car_service.update_car(car_id, car)


@router.delete("/{car_id}", status_code=204)
async def delete_car(car_id: int):
    return car_service.delete_car(car_id)
