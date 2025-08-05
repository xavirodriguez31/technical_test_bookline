from fastapi import FastAPI
from .routers import cars, bookings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s  –  %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Car Rental Service API")

# Include routers
app.include_router(cars.router)
app.include_router(bookings.router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"status": "ok", "message": "Service up and running"}