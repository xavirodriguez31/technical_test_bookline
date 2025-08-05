import json
import logging
from pathlib import Path
from typing import List
from pydantic import BaseModel


logger = logging.getLogger(__name__)


DATA_DIR = Path(__file__).parent.parent.parent / "data"

def _load_file(filename: str) -> list:
    """Load the data from the indicated JSON file"""

    logger.info(f"Loading data from {filename}.")

    path = DATA_DIR / filename
    if not path.exists():
        logger.warning(f"Path: {path} does not exist.")
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Data from {filename} loaded successfully.")
            return data
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {e}")
        return []


def _save_file(filename: str, data: list) -> None:
    """Save the data on the indicated JSON file"""

    logger.info(f"Saving data on {filename}.")

    try:
        DATA_DIR.mkdir(exist_ok=True)
        path = DATA_DIR / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Data saved on {filename}.")

    except Exception as e:
        logger.error(f"Error saving data on JSON: {e}")