import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.ERROR,
    filename="errors.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)
