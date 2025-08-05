from fastapi import APIRouter, HTTPException, status
from ..models import Booking
from ..data_access.bookings import create_booking
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/new_booking", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking_endpoint(booking: Booking):
    """Create a new booking"""

    logger.info(f"/bookings/new_booking endpoint called. Car: {booking.car_id}, Customer: {booking.customer_email}")
    try:
        created_booking = create_booking(booking)
        logger.info(f"Booking created successfully with ID: {created_booking.id}")
        return created_booking
    except ValueError as e:
        logger.warning(f"Validation error creating booking: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 