from typing import List
from ..models import Customer
import logging
from .utils import _load_file, _save_file

logger = logging.getLogger(__name__)

def _load_customers() -> List[Customer]:
    """Load customers from JSON file"""
    customers = _load_file("customers.json")
    return [Customer(**customer) for customer in customers]

def _save_customers(customers: List[Customer]) -> None:
    """Save customers to JSON file"""
    customers_data = [customer.dict() for customer in customers]
    _save_file("customers.json", customers_data)

def get_customer(customer_id: int) -> Customer:
    """Get a specific customer by ID"""
    logger.info(f"Searching customer with ID: {customer_id}.")
    customers = _load_customers()
    for customer in customers:
        if customer.id == customer_id:
            logger.info(f"Customer with ID {customer_id} found.")
            return customer
    
    logger.warning(f"Customer with ID {customer_id} not found.")
    return None

def create_customer(customer: Customer) -> Customer:
    """Create a new customer"""
    logger.info(f"Creating new customer: {customer.email}")
    
    # Check if the email is already registered
    customers = _load_customers()
    emails = [c.email for c in customers]
    if customer.email in emails:
        logger.warning(f"Email already registered.")
        raise ValueError("Email already registered.")
    else:
        # Generate the new ID
        customer.id = max([c.id for c in customers], default=0) + 1
        # Add to db
        customers.append(customer)
        _save_customers(customers)
        
        logger.info(f"Customer created successfully with ID: {customer.id}")
        return customer
