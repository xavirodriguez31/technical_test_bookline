import pytest
from fastapi.testclient import TestClient
from code.models import Car, CarStatus
from code.data_access.cars import create_car, get_available_cars, get_car

class TestCarsEndpoints:
    """Tests for cars endpoints"""
    
    def test_available_cars_empty(self, client):
        """Getting available cars when is empty"""
        response = client.get("/cars/list_availables")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_available_cars_with_data(self, client, sample_car_data):
        """Getting available cars with data"""
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        
        # Get available cars
        response = client.get("/cars/list_availables")
        assert response.status_code == 200
        cars = response.json()
        assert len(cars) == 1 # We have only defined one car
        assert cars[0]["brand"] == sample_car_data["brand"]
        assert cars[0]["status"] == "Available"
    
    def test_create_car_success(self, client, sample_car_data):
        """Creating a car successfully"""
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        
        car = response.json()
        assert car["brand"] == sample_car_data["brand"]
        assert car["model"] == sample_car_data["model"]
        assert car["status"] == "Available"
    
    
    def test_car_duplicate_id(self, client, sample_car_data):
        """Creating a car with duplicate ID"""
        sample_car_data["id"] = 1
        
        # Create a car
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 201
        
        # Try to create another car with same ID
        response = client.post("/cars/new_car", json=sample_car_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_car_invalid_data(self, client):
        """Creating a car with invalid data"""
        invalid_data = {
            "brand": "",
            "model": "Model_5",
            "year": 2020,
            "license_plate": "1234YYY",
            "fuel_type": "Gasoline",
            "transmission": "Automatic",
            "price": 50.0
        }
        
        response = client.post("/cars/new_car", json=invalid_data)
        assert response.status_code == 422  # Validation error
    

class TestCarsDataAccess:
    """Tests for cars data access functions"""
    
    def test_create_car_generates_id(self, temp_data_dir):
        """Create_car generates ID automatically"""
        car_data = Car(
            brand="Toyota",
            model="Model_5",
            year=2020,
            license_plate="1234YYY",
            fuel_type="Gasoline",
            transmission="Automatic",
            price=50.0
        )
        
        created_car = create_car(car_data)
        assert created_car.id is not None

    
    def test_get_available_cars(self, temp_data_dir):
        """Getting available cars"""
        # Create a car
        car_data = Car(
            brand="Toyota",
            model="Model_5",
            year=2020,
            license_plate="1234YYY",
            fuel_type="Gasoline",
            transmission="Automatic",
            price=50.0
        )
        create_car(car_data)
        
        # Get available cars
        available_cars = get_available_cars()
        assert len(available_cars) == 1
        assert available_cars[0].status == CarStatus.available
    