import logging
import logging.config
import sys


def initialize() -> logging.Logger:
    logger = logging.getLogger("Venvu API")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.info("Logger initialized")

    return logger


logger = initialize()
