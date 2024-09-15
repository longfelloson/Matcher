import logging

from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncFileHandler

from config import settings

log_format = "%(asctime)s - %(levelname)s - %(message)s - [%(funcName)s:%(lineno)d]"
formatter = Formatter(log_format)

file_handler = AsyncFileHandler(filename=settings.LOGS_FILE_PATH, mode='a+')
file_handler.formatter = formatter

logger = Logger(name="error_logger", level=logging.ERROR)
logger.add_handler(file_handler)
