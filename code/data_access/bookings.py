from typing import List, Tuple
from datetime import datetime, timedelta
from ..models import Booking, BookingStatus, CarStatus
from cars import get_car, update_car_status
from customers import get_customer
import logging
from utils import _load_file, _save_file

logger = logging.getLogger(__name__)

def _load_bookings() -> List[Booking]:
    """Load bookings from JSON file"""
    bookings_data = _load_file("bookings.json")
    return [Booking(**booking) for booking in bookings_data]

def _save_bookings(bookings: List[Booking]) -> None:
    """Save bookings to JSON file"""
    bookings_data = [booking.dict() for booking in bookings]
    _save_file("bookings.json", bookings_data)

def create_booking(booking: Booking) -> Booking:
    """Create a new booking with validations"""
    logger.info(f"Creating booking for car {booking.car_id} and customer {booking.customer_id}.")
    
    # Validate if car exists
    car = get_car(booking.car_id)
    if not car:
        logger.error(f"Car {booking.car_id} not found for booking")
        raise ValueError("Car not found.")
    
    # Validate if car is available
    if car.status != CarStatus.available or not is_car_available(booking.car_id, booking.start_date, booking.end_date):
        logger.warning(f"Car {booking.car_id} is not available.")
        raise ValueError("Car is not available for booking.")
    
    # Validate if customer exists
    customer = get_customer(booking.customer_id)
    if not customer:
        logger.error(f"Customer {booking.customer_id} not found.")
        raise ValueError("Customer not found")
    
    # Validate dates
    if booking.start_date >= booking.end_date:
        logger.warning(f"Invalid booking dates.")
        raise ValueError("Start date must be before end date.")
    
    if booking.start_date < datetime.now():
        logger.warning(f"Booking start date in the past.")
        raise ValueError("Start date cannot be in the past.")

    # Calculate the total days and price
    booking.total_days, booking.total_price = compute_days_price(booking, car)
    
    # Generate the new booking ID
    bookings = _load_bookings()
    booking.id = max([b.id for b in bookings], default=0) + 1
    
    # Add to db
    bookings.append(booking)
    _save_bookings(bookings)
    
    # Update car status to Rented
    update_car_status(booking.car_id, CarStatus.rented)
    
    logger.info(f"Booking created successfully with ID: {booking.id}.")
    return booking

def compute_days_price(booking: Booking, car) -> Tuple[int, float]:
    """Calculate the total number of days and price for the booking"""
    total_days = (booking.end_date - booking.start_date).days

    # Minimum number of booking days is 1
    total_days = total_days if total_days > 0 else 1
    total_price = car.day_price * total_days

    logger.info(f"Booking calculated: {total_days} days, {total_price}€.")
    return total_days, total_price

def is_car_available(car_id: int, start_date: datetime, end_date: datetime) -> bool:
    """Check if a car is available for specific dates"""
    logger.info(f"Checking availability for car with ID: {car_id} from {start_date} to {end_date}.")
    
    bookings = _load_bookings()
    for booking in bookings:
        if (booking.car_id == car_id and 
            booking.status == BookingStatus.active and
            not (end_date <= booking.start_date or start_date >= booking.end_date)):
            logger.warning(f"Car {car_id} not available. Conflicts with booking {booking.id}.")
            return False
    
    logger.info(f"Car {car_id} is available for the requested dates.")
    return True
