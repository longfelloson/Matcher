import logging

from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.ERROR,
    filename=settings.LOGS_FILE_PATH,
    format="%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
)
