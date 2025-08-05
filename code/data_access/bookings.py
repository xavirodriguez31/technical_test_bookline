from typing import List, Tuple
from datetime import date
from ..models import Booking, BookingStatus, CarStatus
from .cars import get_car, update_car_status
import logging
from .utils import _load_file, _save_file

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
    logger.info(f"Creating booking for car {booking.car_id} and customer {booking.customer_email}.")
    
    logger.info(f"Validating data.")
    # Validate if car exists
    car = get_car(booking.car_id)
    if not car:
        raise ValueError(f"Car with ID {booking.car_id} not found.")
    
    # Validate if car is available
    if car.status != CarStatus.available or not is_car_available(booking.car_id, booking.start_date, booking.end_date):
        raise ValueError(f"Car with ID {booking.car_id} is not available for booking.")
    
    # Validate dates
    if booking.start_date >= booking.end_date:
        raise ValueError("Start date must be before end date.")
    
    if booking.start_date < date.today():
        raise ValueError("Start date cannot be in the past.")

    # Set default status if not provided
    if booking.status is None:
        booking.status = BookingStatus.active
        logger.info("Setting default status to Active")

    # Calculate the total days and price
    booking.total_days, booking.total_price = compute_days_price(booking, car)
    
    # Generate the new booking ID
    bookings = _load_bookings()
    if booking.id is None:
        booking.id = max([b.id for b in bookings], default=0) + 1
        logger.info(f"Generated booking ID: {booking.id}")
    else:
        # Check if ID already exists
        existing_ids = [b.id for b in bookings]
        if booking.id in existing_ids:
            raise ValueError(f"Booking ID {booking.id} already registered.")
    
    # Add to db
    bookings.append(booking)
    _save_bookings(bookings)
    
    # Update car status to Rented
    update_car_status(booking.car_id, CarStatus.rented)
    
    logger.info(f"Booking created successfully with ID: {booking.id}.")
    return booking

def delete_booking(booking_id: int) -> bool:
    """Delete a booking and update car status to available"""
    logger.info(f"Deleting booking with ID: {booking_id}")
    
    bookings = _load_bookings()
    booking_to_delete = None
    
    # Find the booking to delete
    for booking in bookings:
        if booking.id == booking_id:
            booking_to_delete = booking
            break
    
    if not booking_to_delete:
        logger.warning(f"Booking with ID {booking_id} not found.")
        return False
    
    # Check if booking is active
    if booking_to_delete.status == BookingStatus.active:
        # Update car status to available
        car_id = booking_to_delete.car_id
        update_car_status(car_id, CarStatus.available)
        logger.info(f"Updated car {car_id} status to Available.")
    
    # Remove booking from list
    bookings = [b for b in bookings if b.id != booking_id]
    _save_bookings(bookings)
    
    logger.info(f"Booking {booking_id} deleted successfully.")
    return True

def compute_days_price(booking: Booking, car) -> Tuple[int, float]:
    """Calculate the total number of days and price for the booking"""
    total_days = (booking.end_date - booking.start_date).days

    # Minimum number of booking days is 1
    total_days = total_days if total_days > 0 else 1
    total_price = car.price * total_days

    logger.info(f"Booking calculated: {total_days} days, {total_price}€.")
    return total_days, total_price

def is_car_available(car_id: int, start_date: date, end_date: date) -> bool:
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
