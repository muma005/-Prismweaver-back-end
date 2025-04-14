import logging
import os

def setup_logging():
    """Configure logging to output to both console and file."""
    logger = logging.getLogger("prismweaver")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("prismweaver.log")

    # Create formatters and add to handlers
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Initialize logger
logger = setup_logging()