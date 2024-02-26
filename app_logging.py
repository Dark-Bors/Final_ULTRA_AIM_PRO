import logging
from datetime import datetime
import os

# Configure the logger
logger = logging.getLogger('application_logger')
logger.setLevel(logging.DEBUG)  # Set the logging level

# Determine the directory of the current script
current_script_path = os.path.dirname(os.path.realpath(__file__))
print("current_script_path", current_script_path) #debugX

# Define the log directory relative to the script's location
log_directory = os.path.join(current_script_path, 'logs')
print("log_directory", log_directory) #debugX


# Check if the log directory exists, if not, create it
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a file handler with a timestamped log file name, saved in the log directory
current_time = datetime.now().strftime("App_log_%d%m%Y_%H%M.log")  # Adjust the format here
log_file_path = os.path.join(log_directory, current_time)  # Construct the path with the log directory
fh = logging.FileHandler(log_file_path, encoding='utf-8')  # Specify UTF-8 encoding here
fh.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Define custom log levels without emojis to avoid encoding issues
logging.addLevelName(logging.INFO, "INFO")
logging.addLevelName(logging.WARNING, "WARNING")
logging.addLevelName(logging.DEBUG, "DEBUG")
logging.addLevelName(logging.CRITICAL, "CRITICAL")
