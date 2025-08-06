import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from code.models import Booking, BookingStatus, Car, CarStatus
from code.data_access.cars import create_car, get_car
from code.data_access.bookings import create_booking, delete_booking, compute_days_price, is_car_available

class TestBookingsEndpoints:
    """Tests for booking endpoints"""
    
    def test_create_booking_success(self, client, sample_car_data, sample_booking_data):
        """Creating a booking successfully"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        car_id = response.json()["id"]
        
        # Create a booking
        sample_booking_data["car_id"] = car_id
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 201
        
        booking = response.json()
        assert booking["car_id"] == car_id
        assert booking["customer_email"] == sample_booking_data["customer_email"]
        assert booking["total_days"] == 2
        assert booking["total_price"] == 100.0
        assert booking["status"] == "Active"
        assert booking["id"] is not None
    
    def test_booking_car_not_found(self, client, sample_booking_data):
        """Creating booking with non-existent car"""
        sample_booking_data["car_id"] = 500
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    def test_booking_invalid_dates(self, client, sample_car_data, sample_booking_data):
        """Creating booking with invalid dates"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        car_id = response.json()["id"]
        
        # End_date before start_date
        sample_booking_data["car_id"] = car_id
        sample_booking_data["start_date"] = "2024-01-22"
        sample_booking_data["end_date"] = "2024-01-20"
        
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 400
        assert "before end date" in response.json()["detail"]
    
    def test_booking_past_date(self, client, sample_car_data, sample_booking_data):
        """Creating booking with past date"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        car_id = response.json()["id"]
        
        # Past date
        sample_booking_data["car_id"] = car_id
        sample_booking_data["start_date"] = "2020-01-01"
        sample_booking_data["end_date"] = "2020-01-02"
        
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 400
        assert "past" in response.json()["detail"]
    
    def test_booking_car_not_available(self, client, sample_car_data, sample_booking_data):
        """Creating booking for car not available"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        car_id = response.json()["id"]
        
        # Create a booking
        sample_booking_data["car_id"] = car_id
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 201
        
        # Try to create second booking for same car and dates
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 400
        assert "not available" in response.json()["detail"]
    
    def test_delete_booking_success(self, client, sample_car_data, sample_booking_data):
        """Deleting a booking successfully"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        car_id = response.json()["id"]
        
        # Create a booking
        sample_booking_data["car_id"] = car_id
        response = client.post("/bookings/new_booking", json=sample_booking_data)
        assert response.status_code == 201
        booking_id = response.json()["id"]
        
        # Delete booking
        response = client.delete(f"/bookings/delete_booking/{booking_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    

class TestBookingsDataAccess:
    """Tests for booking data access functions"""
    
    def test_compute_days_price(self, temp_data_dir):
        """Computing days and price for booking"""
        # Create a car
        car = Car(
            brand="Sample",
            model="Sample_Model",
            year=2020,
            license_plate="1234KKK",
            fuel_type="Gasoline",
            transmission="Automatic",
            price=30.0
        )
        
        # Create booking
        booking = Booking(
            car_id=1,
            customer_email="test@example.com",
            start_date=date(2025, 9, 20),
            end_date=date(2025, 9, 22)
        )
        
        total_days, total_price = compute_days_price(booking, car)
        assert total_days == 2
        assert total_price == 60.0
    
    def test_car_available(self, temp_data_dir):
        """Car availability"""
        start_date = date(2025, 9, 20)
        end_date = date(2025, 9, 22)
        car_id = 1
        
        is_available = is_car_available(car_id, start_date, end_date)
        assert is_available == True
    
    def test_create_booking_default_status(self, temp_data_dir):
        """Create booking with default status when not provided"""
        # Create a car
        car = Car(
            brand="Test Brand",
            model="Test Model",
            year=2020,
            license_plate="TEST123",
            fuel_type="Gasoline",
            transmission="Automatic",
            price=50.0
        )
        created_car = create_car(car)
        
        # Create booking without status
        booking = Booking(
            car_id=created_car.id,
            customer_email="test@example.com",
            start_date=date(2025, 9, 20),
            end_date=date(2025, 9, 22)
        )
        
        created_booking = create_booking(booking)
        assert created_booking.status == BookingStatus.active
    
    def test_delete_booking_updates_car_status(self, temp_data_dir):
        """Deleting booking updates car status"""
        # Create a car
        car = Car(
            brand="Test Brand",
            model="Test Model",
            year=2020,
            license_plate="TEST123",
            fuel_type="Gasoline",
            transmission="Automatic",
            price=50.0
        )
        created_car = create_car(car)
        
        # Create booking
        booking = Booking(
            car_id=created_car.id,
            customer_email="test@example.com",
            start_date=date(2025, 9, 20),
            end_date=date(2025, 9, 22)
        )
        created_booking = create_booking(booking)
        
        # Delete booking
        success = delete_booking(created_booking.id)
        assert success == True
        
        # Verify car is available again
        updated_car = get_car(created_car.id)
        assert updated_car.status == CarStatus.available 