"""
wait-related commands with dynamic selector support
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger
from commands.element_commands import ElementCommands
from utils.helpers import retry

logger = Logger(__name__)

class WaitCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.element_commands = ElementCommands(driver, config)
    
    @retry
    def wait_for_element_visible(self, selector, selector_type=None, timeout=None):
        """
        Wait for an element to be visible
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The element if visible, None otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to be visible with {by_method}: {selector_value}")
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located((by_method, selector_value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element to be visible with {by_method}: {selector_value}")
            return None
    
    @retry
    def wait_for_element_invisible(self, selector, selector_type=None, timeout=None):
        """
        Wait for an element to be invisible
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is invisible
            
        Raises:
            TimeoutException: If element is still visible after timeout (will be caught by retry decorator)
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to be invisible with {by_method}: {selector_value}")
        try:
            result = WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located((by_method, selector_value))
            )
            return result
        except TimeoutException as e:
            logger.warning(f"Timeout waiting for element to be invisible with {by_method}: {selector_value}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Element still visible after {wait_time} seconds: {by_method}:{selector_value}")
    
    @retry
    def wait_for_element_present(self, selector, selector_type=None, timeout=None):
        """
        Wait for an element to be present in the DOM
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The element if present, None otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to be present with {by_method}: {selector_value}")
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by_method, selector_value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element to be present with {by_method}: {selector_value}")
            return None
    
    @retry
    def wait_for_element_clickable(self, selector, selector_type=None, timeout=None):
        """
        Wait for an element to be clickable
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The element if clickable, None otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to be clickable with {by_method}: {selector_value}")
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((by_method, selector_value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout waiting for element to be clickable with {by_method}: {selector_value}")
            return None
    
    @retry
    def wait_for_text(self, selector, text, selector_type=None, timeout=None):
        """
        Wait for an element to contain the specified text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The text to wait for
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
            
        Returns:
            True if text found
            
        Raises:
            TimeoutException: If text not found after timeout (will be caught by retry decorator)
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for text '{text}' in element with {by_method}: {selector_value}")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element((by_method, selector_value), text)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for text '{text}' in element with {by_method}: {selector_value}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Text '{text}' not found in element after {wait_time} seconds: {by_method}:{selector_value}")
    
    def wait_for_attribute(self, selector, attribute, value, selector_type=None, timeout=None):
        """
        Wait for an element to have a specific attribute value
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            attribute: The attribute name to check
            value: The attribute value to wait for
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if attribute has the value, False otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to have attribute '{attribute}' with value '{value}' with {by_method}: {selector_value}")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element_attribute((by_method, selector_value), attribute, value)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for attribute '{attribute}' with value '{value}' with {by_method}: {selector_value}")
            return False
    
    def wait_for_url(self, url, timeout=None):
        """
        Wait for the URL to match the expected URL
        
        Args:
            url: The expected URL
            timeout: Optional timeout in seconds
            
        Returns:
            True if URL matches
            
        Raises:
            TimeoutException: If URL doesn't match after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for URL to be: {url}")
        
        def check_url():
            current_url = self.driver.current_url
            return current_url == url
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_url)
        except TimeoutException:
            current_url = self.driver.current_url
            logger.warning(f"Timeout waiting for URL to be: {url}. Current URL: {current_url}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"URL didn't match after {wait_time} seconds. Expected: {url}, Got: {current_url}")
    
    def wait_for_url_contains(self, partial_url, timeout=None):
        """
        Wait for the URL to contain a specific substring
        
        Args:
            partial_url: The substring to look for in the URL
            timeout: Optional timeout in seconds
            
        Returns:
            True if URL contains the substring
            
        Raises:
            TimeoutException: If URL doesn't contain the substring after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for URL to contain '{partial_url}'")
        
        def check_url_contains():
            current_url = self.driver.current_url
            return partial_url in current_url
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_url_contains)
        except TimeoutException:
            current_url = self.driver.current_url
            logger.warning(f"Timeout waiting for URL to contain '{partial_url}'. Current URL: {current_url}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"URL doesn't contain substring after {wait_time} seconds. Expected to contain: '{partial_url}', Got: '{current_url}'")
    
    def wait_for_title(self, title, timeout=None):
        """
        Wait for the page title to match a specific value
        
        Args:
            title: The expected title
            timeout: Optional timeout in seconds
            
        Returns:
            True if title matches
            
        Raises:
            TimeoutException: If title doesn't match after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for title to be '{title}'")
        
        def check_title():
            current_title = self.driver.title
            return current_title == title
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_title)
        except TimeoutException:
            current_title = self.driver.title
            logger.warning(f"Timeout waiting for title to be '{title}'. Current title: '{current_title}'")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Title didn't match after {wait_time} seconds. Expected: '{title}', Got: '{current_title}'")
    
    def wait_for_title_contains(self, partial_title, timeout=None):
        """
        Wait for the page title to contain a specific substring
        
        Args:
            partial_title: The substring to look for in the title
            timeout: Optional timeout in seconds
            
        Returns:
            True if title contains the substring
            
        Raises:
            TimeoutException: If title doesn't contain the substring after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for title to contain '{partial_title}'")
        
        def check_title_contains():
            current_title = self.driver.title
            return partial_title in current_title
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_title_contains)
        except TimeoutException:
            current_title = self.driver.title
            logger.warning(f"Timeout waiting for title to contain '{partial_title}'. Current title: '{current_title}'")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Title doesn't contain substring after {wait_time} seconds. Expected to contain: '{partial_title}', Got: '{current_title}'")
    
    def wait(self, seconds):
        """
        Wait for a specific number of seconds
        
        Args:
            seconds: The number of seconds to wait
            
        Returns:
            True always
        """
        logger.info(f"Waiting for {seconds} seconds")
        time.sleep(seconds)
        return True
    
    def wait_for_elements_count(self, selector, count, selector_type=None, timeout=None):
        """
        Wait for the number of elements matching a selector to equal the expected count
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            count: The expected number of elements
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
            
        Returns:
            True if element count matches
            
        Raises:
            TimeoutException: If element count doesn't match after timeout (will be caught by retry decorator)
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element count to equal {count} with {by_method}: {selector_value}")
        
        def check_element_count():
            elements = self.driver.find_elements(by_method, selector_value)
            return len(elements) == count
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_element_count)
        except TimeoutException:
            elements = self.driver.find_elements(by_method, selector_value)
            actual_count = len(elements)
            logger.warning(f"Timeout waiting for element count to equal {count}. Actual count: {actual_count}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Element count didn't match after {wait_time} seconds. Expected: {count}, Got: {actual_count}")
    
    def wait_for_elements_count_greater_than(self, selector, min_count, selector_type=None, timeout=None):
        """
        Wait for the number of elements matching a selector to be greater than the specified count
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            min_count: The minimum number of elements expected
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
            
        Returns:
            True if element count is greater than min_count
            
        Raises:
            TimeoutException: If element count is not greater than min_count after timeout (will be caught by retry decorator)
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element count to be greater than {min_count} with {by_method}: {selector_value}")
        
        def check_element_count_greater_than():
            elements = self.driver.find_elements(by_method, selector_value)
            return len(elements) > min_count
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_element_count_greater_than)
        except TimeoutException:
            elements = self.driver.find_elements(by_method, selector_value)
            actual_count = len(elements)
            logger.warning(f"Timeout waiting for element count to be greater than {min_count}. Actual count: {actual_count}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"Element count not greater than minimum after {wait_time} seconds. Expected > {min_count}, Got: {actual_count}")
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait for the page to finish loading
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            True if page loaded
            
        Raises:
            TimeoutException: If page doesn't load after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.PAGE_LOAD_TIMEOUT
        
        logger.info("Waiting for page to load")
        
        def is_page_loaded():
            return self.driver.execute_script("return document.readyState") == "complete"
        
        try:
            return WebDriverWait(self.driver, wait_time).until(is_page_loaded)
        except TimeoutException:
            logger.warning("Timeout waiting for page to load")
            # Raise the exception so the retry decorator can catch it
            current_state = self.driver.execute_script("return document.readyState")
            raise TimeoutException(f"Page didn't load after {wait_time} seconds. Current state: {current_state}")
    
    def wait_for_ajax(self, timeout=None):
        """
        Wait for all AJAX requests to complete (jQuery)
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            True if all AJAX requests completed
            
        Raises:
            TimeoutException: If AJAX requests are still running after timeout (will be caught by retry decorator)
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info("Waiting for AJAX requests to complete")
        
        def are_ajax_requests_complete():
            return self.driver.execute_script("return (typeof jQuery === 'undefined' || jQuery.active === 0)")
        
        try:
            return WebDriverWait(self.driver, wait_time).until(are_ajax_requests_complete)
        except TimeoutException:
            ajax_count = self.driver.execute_script("return (typeof jQuery !== 'undefined') ? jQuery.active : 0")
            logger.warning(f"Timeout waiting for AJAX requests to complete. Active requests: {ajax_count}")
            # Raise the exception so the retry decorator can catch it
            raise TimeoutException(f"AJAX requests still running after {wait_time} seconds. Active requests: {ajax_count}")