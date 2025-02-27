"""
Configuration settings for the Flask Selenium testing framework
"""

import os

class Config:
    # Browser settings
    DEFAULT_BROWSER = "chrome"
    HEADLESS = os.environ.get("HEADLESS", "True").lower() == "false"
    IMPLICIT_WAIT = int(os.environ.get("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))
    
    # Screenshot settings
    SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "screenshots")
    TAKE_SCREENSHOT_ON_FAILURE = os.environ.get("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    
    # Retry settings
    MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.environ.get("RETRY_DELAY", "1"))
