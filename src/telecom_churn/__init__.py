import os
import sys
import logging

logging_str = "[%(asctime)s : %(levelname)s : %(module)s : %(message)s]"

log_dir = "logs" # directory for logs
log_filepath = os.path.join(log_dir, "logging.log") # log file path
os.makedirs(log_dir, exist_ok=True) # create logs directory if not exists

logging.basicConfig(
    level = logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath), # log file handler to write logs to a file
        logging.StreamHandler(sys.stdout) # stream handler to output logs to console
    ]
)

logger = logging.getLogger("datascience")
