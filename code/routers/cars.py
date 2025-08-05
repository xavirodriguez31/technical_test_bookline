from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Car
from ..data_access.cars import get_available_cars, create_car, get_car
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("/list_availables", response_model=List[Car])
async def get_available_cars_endpoint():
    """Get all cars that are available for booking"""
    logger.info("GET /cars/available endpoint called")
    try:
        available_cars = get_available_cars()
        logger.info(f"Successfully returned {len(available_cars)} available cars.")
        return available_cars
    except Exception as e:
        logger.error(f"Error getting available cars. {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/new_car", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car_endpoint(car: Car):
    """Create a new car"""
    logger.info(f"POST /cars/new_car endpoint called. Creating car: {car.brand} {car.model}")
    try:
        created_car = create_car(car)
        logger.info(f"Car created successfully with ID: {created_car.id}")
        return created_car
    except ValueError as e:
        logger.warning(f"Validation error creating car. {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating car. {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 