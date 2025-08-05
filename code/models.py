from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Predefined values

class CarStatus(str, Enum):
    available = "Available"
    rented = "Rented"
    maintenance = "Maintenance"
    out_of_service = "Out_of_Service"

class Fuel(str, Enum):
    gasoline = "gasoline"
    diesel = "diesel"
    electric = "electric"
    hybrid = "hybrid"

class Transmission(str, Enum):
    manual = "manual"
    automatic = "automatic"

class BookingStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


# Main models

class Car(BaseModel):
    id: Optional[int] = Field(None, description="Car ID, unique")
    brand: str = Field(..., max_length=50, description="Brand of the car")
    model: str = Field(..., max_length=50, description="Model of the car")
    year: int = Field(..., ge=1800, le=2050, description="Year of the car")
    license_plate: str = Field(..., min_length=5, max_length=10, description="License Plate of the car")
    fuel_type: Fuel = Field(..., description="Fuel type of the car")
    transmission: Transmission = Field(..., description="Transmission type of the car") 
    day_price: float = Field(..., gt=0, description="Rental price per day")
    status: CarStatus = Field(default=CarStatus.available, description="Car Status")
    updated_at: Optional[datetime] = Field(None, description="Date of the last car update")

    class Config:
        from_attributes = True

class Customer(BaseModel):
    id: Optional[int] = Field(None, description="Customer ID, unique")
    email: str = Field(..., description="Email of the Customer")
    first_name: str = Field(..., min_length=1, max_length=50, description="Customer Name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Customer Last Name")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number of the Customer")
    updated_at: Optional[datetime] = Field(None, description="Date of the last customer update")

    class Config:
        from_attributes = True

class Booking(BaseModel):
    id: Optional[int] = Field(None, description="Booking ID, unique")
    car_id: int = Field(..., description="Rented Car ID")
    customer_id: int = Field(..., description="Customer ID")
    start_date: datetime = Field(..., description="Start date of the booking")
    end_date: datetime = Field(..., description="End date of the booking")
    total_days: float = Field(..., gt=0, description="Total booking days")
    total_price: float = Field(..., gt=0, description="Total booking price")
    status: BookingStatus = Field(default=BookingStatus.active, description="Status of the booking")
    updated_at: Optional[datetime] = Field(None, description="Date of the last booking update")

    class Config:
        from_attributes = True