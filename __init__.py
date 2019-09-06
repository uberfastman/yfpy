import logging
import os
from logging.handlers import RotatingFileHandler

# configure root logger settings
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stderr_logger = logging.getLogger("STDERR")
stderr_logger.setLevel(logging.ERROR)

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# console handler
console_handler = logging.StreamHandler()  # can put sys.stdout or sys.stderr as parameter of StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# stdout log file handler
stdout_file_handler = RotatingFileHandler(os.path.join(log_dir, "out.log"), maxBytes=1000000, backupCount=5, mode="a")
stdout_file_handler.setLevel(logging.INFO)
stdout_file_handler.setFormatter(log_formatter)
logger.addHandler(stdout_file_handler)

# stderr log file handler
stderr_file_handler = RotatingFileHandler(os.path.join(log_dir, "error.log"), maxBytes=100000, backupCount=5, mode="a")
stderr_file_handler.setLevel(logging.ERROR)
stderr_file_handler.setFormatter(log_formatter)
stderr_logger.addHandler(stderr_file_handler)
