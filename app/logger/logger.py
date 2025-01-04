import logging

logging.basicConfig(
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler()  # Optional: Also log to console
    ]
)

# Create a logger
logger = logging.getLogger("Pyto API")