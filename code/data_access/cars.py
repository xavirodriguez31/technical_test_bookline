from typing import List
from ..models import Car, CarStatus
import logging
from .utils import _load_file, _save_file

logger = logging.getLogger(__name__)

def _load_cars() -> List[Car]:
    """Load cars from JSON file"""
    cars_data = _load_file("cars.json")
    return [Car(**car) for car in cars_data]

def _save_cars(cars: List[Car]) -> None:
    """Save cars to JSON file"""
    cars_data = [car.dict() for car in cars]
    _save_file("cars.json", cars_data)

def get_available_cars() -> List[Car]:
    """Get all the cars that are available"""
    logger.info("Searching available cars.")
    cars = _load_cars()
    available_cars = [car for car in cars if car.status == CarStatus.available]
    logger.info(f"{len(available_cars)} available cars found.")
    return available_cars

def get_car(car_id: int) -> Car:
    """Get a specific car by ID"""
    logger.info(f"Searching car with ID: {car_id}.")
    cars = _load_cars()
    for car in cars:
        if car.id == car_id:
            logger.info(f"Car with ID {car_id} found.")
            return car
    
    logger.warning(f"Car with ID {car_id} not found.")
    return None

def create_car(car: Car) -> Car:
    """Create a new car"""
    logger.info(f"Creating new car.")
    
    cars = _load_cars()
    # Check the new ID
    ids = [c.id for c in cars]
    if car.id in ids:
        raise ValueError(f"ID {car.id} already registered.")
    # Add to db
    cars.append(car)
    _save_cars(cars)
    
    logger.info(f"Car created successfully with ID: {car.id}")
    return car

def update_car_status(car_id: int, status: CarStatus) -> bool:
    """Update car status"""
    logger.info(f"Updating car {car_id} status to: {status}.")
    
    cars = _load_cars()
    for car in cars:
        if car.id == car_id:
            car.status = status
            _save_cars(cars)
            logger.info(f"Car status updated successfully.")
            return True
    
    logger.warning(f"Car with ID: {car_id} not found.")
    return False
