"""
wait-related commands with dynamic selector support
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger
from commands.element_commands import ElementCommands

logger = Logger(__name__)

class WaitCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.element_commands = ElementCommands(driver, config)
    
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
    
    def wait_for_element_invisible(self, selector, selector_type=None, timeout=None):
        """
        Wait for an element to be invisible
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is invisible, False if still visible
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to be invisible with {by_method}: {selector_value}")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located((by_method, selector_value))
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for element to be invisible with {by_method}: {selector_value}")
            return False
    
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
    
    def wait_for_text(self, selector, text, selector_type=None, timeout=None):
        """
        Wait for an element to contain specific text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The text to wait for
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if text is present, False otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element to contain text '{text}' with {by_method}: {selector_value}")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element((by_method, selector_value), text)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for text '{text}' in element with {by_method}: {selector_value}")
            return False
    
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
        Wait for the URL to match a specific value
        
        Args:
            url: The URL to wait for
            timeout: Optional timeout in seconds
        
        Returns:
            True if URL matches, False otherwise
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for URL to match '{url}'")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.url_to_be(url)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for URL to match '{url}'")
            return False
    
    def wait_for_url_contains(self, partial_url, timeout=None):
        """
        Wait for the URL to contain a specific value
        
        Args:
            partial_url: The text that should be contained in the URL
            timeout: Optional timeout in seconds
        
        Returns:
            True if URL contains partial URL, False otherwise
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for URL to contain '{partial_url}'")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(partial_url)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for URL to contain '{partial_url}'")
            return False
    
    def wait_for_title(self, title, timeout=None):
        """
        Wait for the page title to match a specific value
        
        Args:
            title: The title to wait for
            timeout: Optional timeout in seconds
        
        Returns:
            True if title matches, False otherwise
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for title to match '{title}'")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.title_is(title)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for title to match '{title}'")
            return False
    
    def wait_for_title_contains(self, partial_title, timeout=None):
        """
        Wait for the page title to contain a specific value
        
        Args:
            partial_title: The text that should be contained in the title
            timeout: Optional timeout in seconds
        
        Returns:
            True if title contains partial title, False otherwise
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for title to contain '{partial_title}'")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.title_contains(partial_title)
            )
        except TimeoutException:
            logger.warning(f"Timeout waiting for title to contain '{partial_title}'")
            return False
    
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
            True if element count matches, False otherwise
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
            logger.warning(f"Timeout waiting for element count to equal {count}. Actual count: {len(elements)}")
            return False
    
    def wait_for_elements_count_greater_than(self, selector, min_count, selector_type=None, timeout=None):
        """
        Wait for the number of elements matching a selector to be greater than min_count
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            min_count: The minimum expected number of elements
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
            
        Returns:
            True if element count is greater than min_count, False otherwise
        """
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Waiting for element count to be greater than {min_count} with {by_method}: {selector_value}")
        
        def check_element_count():
            elements = self.driver.find_elements(by_method, selector_value)
            return len(elements) > min_count
        
        try:
            return WebDriverWait(self.driver, wait_time).until(check_element_count)
        except TimeoutException:
            elements = self.driver.find_elements(by_method, selector_value)
            logger.warning(f"Timeout waiting for element count to be greater than {min_count}. Actual count: {len(elements)}")
            return False
    
    def wait_for_page_load(self, timeout=None):
        """
        Wait for the page to finish loading
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            True if page loaded, False on timeout
        """
        wait_time = timeout if timeout is not None else self.config.PAGE_LOAD_TIMEOUT
        
        logger.info("Waiting for page to load")
        
        def is_page_loaded():
            return self.driver.execute_script("return document.readyState") == "complete"
        
        try:
            return WebDriverWait(self.driver, wait_time).until(is_page_loaded)
        except TimeoutException:
            logger.warning("Timeout waiting for page to load")
            return False
    
    def wait_for_ajax(self, timeout=None):
        """
        Wait for all AJAX requests to complete (jQuery)
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            True if all AJAX requests completed, False on timeout
        """
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info("Waiting for AJAX requests to complete")
        
        def are_ajax_requests_complete():
            return self.driver.execute_script("return (typeof jQuery === 'undefined' || jQuery.active === 0)")
        
        try:
            return WebDriverWait(self.driver, wait_time).until(are_ajax_requests_complete)
        except TimeoutException:
            logger.warning("Timeout waiting for AJAX requests to complete")
            return False