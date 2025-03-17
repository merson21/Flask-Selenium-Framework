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
import functools
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException, 
                                      ElementNotVisibleException, ElementNotInteractableException)
from utils.logger import Logger

def take_screenshot(driver, name=None):
    """
    Take a screenshot of the current browser window
    """
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name or 'screenshot'}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename

def retry(func=None, max_retries=None, delay=None):
    """
    Retry decorator for element commands
    
    Can be used as @retry or with parameters @retry(max_retries=5, delay=2)
    
    Args:
        func: The function to decorate
        max_retries: Maximum number of retry attempts (defaults to Config.MAX_RETRIES)
        delay: Delay between retries in seconds (defaults to Config.RETRY_DELAY)
    """
    # Handle case when decorator is used without arguments
    if func is not None:
        return retry()(func)
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get retry settings from config if available
            retries = max_retries
            if retries is None and hasattr(self, 'config') and hasattr(self.config, 'MAX_RETRIES'):
                retries = self.config.MAX_RETRIES
            else:
                retries = 3  # Default fallback
                
            retry_delay = delay
            if retry_delay is None and hasattr(self, 'config') and hasattr(self.config, 'RETRY_DELAY'):
                retry_delay = self.config.RETRY_DELAY
            else:
                retry_delay = 1  # Default fallback
            
            last_exception = None
            logger = Logger(__name__)
            
            # Log the function call for debugging
            arg_str = ', '.join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])
            logger.info(f"RETRY-PROTECTED: Calling {func.__name__}({arg_str})")
            
            for attempt in range(retries):
                try:
                    if attempt > 0:
                        logger.warning(f"RETRY ATTEMPT {attempt}/{retries-1} for {func.__name__}")
                    
                    result = func(self, *args, **kwargs)
                    
                    if attempt > 0:
                        logger.warning(f"RETRY SUCCEEDED on attempt {attempt+1}/{retries} for {func.__name__}")
                    
                    return result
                    
                except (NoSuchElementException, StaleElementReferenceException, 
                        ElementNotVisibleException, ElementNotInteractableException,
                        TimeoutException) as e:
                    last_exception = e
                    if attempt < retries - 1:
                        logger.warning(f"RETRY TRIGGERED: Attempt {attempt+1}/{retries} failed for {func.__name__}: {str(e)}")
                        logger.warning(f"Waiting {retry_delay}s before retry {attempt+2}/{retries}")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"RETRY EXHAUSTED: All {retries} attempts failed for {func.__name__}")
                except Exception as e:
                    # For other exceptions, don't retry
                    logger.error(f"NON-RETRYABLE ERROR in {func.__name__}: {str(e)}")
                    raise
            
            # If we've exhausted all retries, log and re-raise the last exception
            logger.error(f"RETRY FAILED: All {retries} attempts failed for {func.__name__}: {str(last_exception)}")
            raise last_exception
        
        return wrapper
    
    return decorator

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
