"""
Helper utilities for the framework
"""

import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def take_screenshot(driver, name=None):
    """
    Take a screenshot of the current browser window
    """
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name or 'screenshot'}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename

def retry(func, max_retries=3, delay=1):
    """
    Retry a function execution with delay between retries
    """
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    time.sleep(delay)
        raise last_exception
    return wrapper

def wait_for_element(driver, locator, timeout=10):
    """
    Wait for an element to be present and visible
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None
