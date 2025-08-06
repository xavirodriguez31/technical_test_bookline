# Car Rental Service API

The Car Rental Service API is an application built with FastAPI in Python to simulate the management of a car rental service. This application include the following key features:

- **Car management**: create a new car, list available cars.
- **Booking management**: create a new booking, delete a booking.
- All the data stored in **JSON files**.
- **Tests**: Some defined Unit and Integration tests. 
- **Docker support** for containerized deployment. 

## Repository Structure

The Github repository is organized in three main sections:

- **Code**: Contains the application source code, including entry point, model schemas, routers, and data access functions. It is organized into:
  - `data_access/`: Contains modules for interact with JSON files and some other logics.
  - `routers/`: Contains the route endpoints for cars and bookings.
  - Core files: `main.py` and `models.py`, containing the app entry point and the model schemas.
- **Data**: Contains the JSON files with the data stored.
- **Tests**: Contains unit and integration tests implemented using Pytest.



## Local Setup 

1. **Prerequisites**

- Python installed.
- Docker installed (for containerized deployment)

2. **Clone the repository and create virtual environment**

```bash
git clone <url>
cd technical_test_bookline

python -m venv -venv
.venv\Scripts\activate # For Windows
``` 

3. **Install Requirements**

```bash
pip install -r requirements.txt
```

4. **Run API**

```bash
uvicorn code.main:app --reload --port 8000
```

5. **Access the API**

Open the browser and copy: http://127.0.0.1:8000/docs. Here you can see and execute all the available endpoints. 


## API Endpoints

### Cars

- `/cars/list_availables`: Return a list of all the cars with available status in JSON format. 
- `/cars/new_car`: Creates a new car. The car details must be given in JSON format.All the fields must be provided, except from the `id` which can be computed automatically. Here is an example of input:

```bash
{
    "brand": "Toyota",
    "model": "Model_5",
    "year": 2020,
    "license_plate": "1234YYY",
    "fuel_type": "Gasoline",
    "transmission": "Automatic",
    "price": 50.0
}
```

### Booking

- `/bookings/new_booking`: Creates a new booking. The booking details must be given in JSON format. The required fields are `customer_email`, `start_date` and `end_date`. The other fields will be computed automatically. Here is an example of input:
```bash
{
    "customer_email": "test@example.com",
    "start_date": "2025-09-20",
    "end_date": "2025-09-22"
}
```
- `/bookings/delete_booking/{booking_id}`: Deletes an existing booking with the indicated id. The status of the afected car is updated to Available.

#### Constraints

- No past dates are allowed to create a booking
- The mininum number of booking days is 1

## Logging

All the code is accompanied by logging statements that record the key operations, enabling full control and visibility into the execution at all times. 


## Tests

The application include some tests, implemented using Pytest. These tests include:

- **Unit Tests**: testing internal `data_accesss` modules.
- **Integration Tests**: testing the endpoints.

To run the tests the `pytest.ini` file have to be executed with the following command.
```bash
pytest
```

## Containerization

To containerize the application using Docker the following steps should be followed:

1. **Build image**
```bash
docker build -t car-rental-service-api:latest .
```
2. **Run container**
```bash
docker run -d --name car-api -p 8000:8000 car-rental-service-api:latest
```

3. **Open API** 

Open the browser and copy: http://localhost:8000/docs.

4. **View the logs**
```bash
docker logs -f car-api
```

5. **Stop**
```bash
docker stop car-api
```




