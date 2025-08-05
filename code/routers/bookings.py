from fastapi import APIRouter, HTTPException, status
from ..models import Booking
from ..data_access.bookings import create_booking, delete_booking
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/new_booking", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking_endpoint(booking: Booking):
    """Create a new booking"""

    logger.info(f"POST /bookings/ endpoint called. Car: {booking.car_id}, Customer: {booking.customer_email}")
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

@router.delete("/delete_booking/{booking_id}")
async def delete_booking_endpoint(booking_id: int):
    """Delete a booking and update car status to available"""
    logger.info(f"DELETE /bookings/{booking_id} endpoint called.")
    try:
        success = delete_booking(booking_id)
        if success:
            logger.info(f"Booking {booking_id} deleted successfully.")
            return {"message": f"Booking {booking_id} deleted successfully."}
        else:
            logger.warning(f"Booking {booking_id} not found.")
            raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found.")
    except Exception as e:
        logger.error(f"Error deleting booking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 