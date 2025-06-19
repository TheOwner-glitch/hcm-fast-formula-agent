import logging
import os

def setup_logger(log_file="app.log"):
    logger = logging.getLogger("FastFormulaLogger")
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers in debug mode
    if not logger.handlers:
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger