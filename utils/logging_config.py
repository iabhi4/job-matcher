import os
import logging

log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_directory, exist_ok=True)

log_file_path = os.path.join(log_directory, 'app.log')
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file_path),
                        logging.StreamHandler()
                    ])

def get_logger(name):
    return logging.getLogger(name)
