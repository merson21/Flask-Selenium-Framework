"""
Helper utilities for the framework
"""

import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.exceptions import ElementTimeoutException

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

def wait_for_element(driver, locator, timeout=10, raise_exception=False, config=None):
    """
    Wait for an element to be present and visible
    
    Args:
        driver: Selenium WebDriver instance
        locator: Tuple of (By method, selector value)
        timeout: Timeout in seconds
        raise_exception: Whether to raise an exception if element not found
        config: Config object with IMPLICIT_WAIT setting
        
    Returns:
        The element if found, None otherwise
        
    Raises:
        ElementTimeoutException: If raise_exception is True and element not found
    """
    # Set implicit wait to 0 to prevent it from interfering with our explicit wait
    driver.implicitly_wait(0)
    
    try:
        # Use explicit wait with the specified timeout
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        if raise_exception:
            by_method, selector_value = locator
            raise ElementTimeoutException(selector_value, by_method, timeout)
        return None
    finally:
        # Restore the implicit wait
        if config and hasattr(config, 'IMPLICIT_WAIT'):
            driver.implicitly_wait(config.IMPLICIT_WAIT)
        else:
            # Use a reasonable default if config is not provided
            driver.implicitly_wait(10)
