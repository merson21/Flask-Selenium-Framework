"""
Logging utility for the framework
"""

import logging
import os
from datetime import datetime

class Logger:
    # Class variable to store the last error message
    last_error = None
    
    # Class variable to store logger instances
    _instances = {}
    
    def __new__(cls, name, log_level=logging.INFO):
        # Implement singleton pattern per logger name
        if name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            cls._instances[name] = instance
            instance._initialized = False
        return cls._instances[name]
    
    def __init__(self, name, log_level=logging.INFO):
        # Skip initialization if already initialized
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers to prevent duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
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
        
        self._initialized = True
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        # Store the error message in the class variable
        Logger.last_error = message
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def critical(self, message):
        # Store critical errors too
        Logger.last_error = message
        self.logger.critical(message)
        
    @classmethod
    def get_last_error(cls):
        """
        Get the last error message
        
        Returns:
            The last error message or None if no errors
        """
        return cls.last_error
        
    @classmethod
    def clear_last_error(cls):
        """
        Clear the last error message
        """
        cls.last_error = None

