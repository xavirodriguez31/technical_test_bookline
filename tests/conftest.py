import pytest
from fastapi.testclient import TestClient
from code.main import app
import code.data_access.utils as utils
import tempfile
import shutil
import os
from pathlib import Path

@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Creates an empty data folder at tmp_path for testing"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for f in ("cars.json", "bookings.json"):
        (data_dir / f).write_text("[]")
    monkeypatch.setattr(utils, "DATA_DIR", data_dir)
    return data_dir

@pytest.fixture
def sample_car_data():
    """Sample car data for tests"""
    return {
        "brand": "Toyota",
        "model": "Model_5",
        "year": 2020,
        "license_plate": "1234YYY",
        "fuel_type": "Gasoline",
        "transmission": "Automatic",
        "price": 50.0
    }

@pytest.fixture
def sample_booking_data():
    """Sample booking data for tests"""
    return {
        "car_id": 1,
        "customer_email": "test@example.com",
        "start_date": "2025-09-20",
        "end_date": "2025-09-22"
    } 