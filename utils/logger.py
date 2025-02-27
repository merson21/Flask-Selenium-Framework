"""
Logging utility for the framework
"""

import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Create file handler
        log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def critical(self, message):
        self.logger.critical(message)

