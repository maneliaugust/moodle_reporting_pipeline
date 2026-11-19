
import logging
import os


def setup_logger():

    # Create logs folder if it does not exist
    os.makedirs("logs", exist_ok=True)

    # Configure log file
    log_file = os.path.join("logs", "moodle_pipeline.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )

    logger = logging.getLogger("moodle_pipeline")

    return logger
