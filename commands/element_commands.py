"""
Element-related commands with dynamic selector support
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import Logger
from utils.helpers import wait_for_element, retry
from utils.exceptions import ElementTimeoutException

logger = Logger(__name__)

class ElementCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
    
    def _get_by_method(self, selector_type):
        """
        Get the appropriate By method based on selector type
        """
        selector_map = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "class": By.CLASS_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        return selector_map.get(selector_type.lower(), By.CSS_SELECTOR)
    
    def _parse_selector(self, selector, selector_type=None):
        """
        Parse selector string based on prefix to determine the selector type and value
        Supported formats:
        - "#element_id" -> (By.ID, "element_id")
        - ".class_name" -> (By.CLASS_NAME, "class_name")
        - "@name_value" -> (By.NAME, "name_value")
        - "//xpath/expression" -> (By.XPATH, "//xpath/expression")
        - "tag.class" or any other CSS -> (By.CSS_SELECTOR, selector)
        
        If selector_type is explicitly provided, it will override the automatic detection.
        """
        if selector_type:
            return self._get_by_method(selector_type), selector
        
        # Auto-detect selector type based on prefix
        if selector.startswith('#') and ' ' not in selector and '>' not in selector and ',' not in selector:
            # ID selector: #element_id
            return By.ID, selector[1:]
        elif selector.startswith('.') and ' ' not in selector and '>' not in selector and ',' not in selector:
            # Class selector: .class_name
            return By.CLASS_NAME, selector[1:]
        elif selector.startswith('@'):
            # Name selector: @name_value
            return By.NAME, selector[1:]
        elif selector.startswith('//') or selector.startswith('(//'):
            # XPath selector: //div[@id='element']
            return By.XPATH, selector
        elif selector.startswith('link='):
            # Link text selector: link=Click Me
            return By.LINK_TEXT, selector[5:]
        elif selector.startswith('partial-link='):
            # Partial link text selector: partial-link=Click
            return By.PARTIAL_LINK_TEXT, selector[13:]
        else:
            # Default to CSS selector
            return By.CSS_SELECTOR, selector
    
    def find(self, selector, selector_type=None, timeout=None, raise_exception=False):
        """
        Find an element using the specified selector
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
            raise_exception: Whether to raise an exception if element not found
        
        Returns:
            The found element or None if not found and raise_exception is False
            
        Raises:
            ElementTimeoutException: If raise_exception is True and element not found
        """
        by_method, selector_value = self._parse_selector(selector, selector_type)
        wait_time = timeout if timeout is not None else self.config.IMPLICIT_WAIT
        
        logger.info(f"Finding element with {By.__name__}.{by_method}: {selector_value}")
        try:
            element = wait_for_element(self.driver, (by_method, selector_value), wait_time, raise_exception, self.config)
            if element:
                return element
            elif raise_exception:
                # This should not happen as wait_for_element should raise an exception
                raise ElementTimeoutException(selector_value, by_method, wait_time)
            else:
                logger.error(f"Element not found with {By.__name__}.{by_method}: {selector_value}")
                return None
        except ElementTimeoutException:
            # Re-raise ElementTimeoutException
            raise
        except Exception as e:
            logger.error(f"Error finding element with {By.__name__}.{by_method}: {selector_value} - {str(e)}")
            if raise_exception:
                raise
            return None
    
    def find_or_fail(self, selector, selector_type=None, timeout=None):
        """
        Find an element using the specified selector or raise an exception if not found
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The found element
            
        Raises:
            ElementTimeoutException: If element not found after timeout
        """
        return self.find(selector, selector_type, timeout, raise_exception=True)
    
    def find_all(self, selector, selector_type=None):
        """
        Find all elements matching the specified selector
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
        
        Returns:
            List of found elements
        """
        by_method, selector_value = self._parse_selector(selector, selector_type)
        
        logger.info(f"Finding all elements with {By.__name__}.{by_method}: {selector_value}")
        try:
            elements = self.driver.find_elements(by_method, selector_value)
            logger.info(f"Found {len(elements)} elements")
            return elements
        except Exception as e:
            logger.error(f"Error finding elements with {By.__name__}.{by_method}: {selector_value} - {str(e)}")
            return []
    
    @retry
    def click(self, selector, selector_type=None, timeout=None):
        """
        Click on an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if click successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.info(f"Clicking on element with {By.__name__}.{by_method}: {selector_value}")
            element.click()
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for click: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def double_click(self, selector, selector_type=None, timeout=None):
        """
        Double-click on an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if double-click successful, False otherwise
        """
        from selenium.webdriver.common.action_chains import ActionChains
        
        element = self.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.info(f"Double-clicking on element with {By.__name__}.{by_method}: {selector_value}")
            ActionChains(self.driver).double_click(element).perform()
            return True
        return False
    
    @retry
    def right_click(self, selector, selector_type=None, timeout=None):
        """
        Right-click on an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if right-click successful, False otherwise
        """
        from selenium.webdriver.common.action_chains import ActionChains
        
        element = self.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.info(f"Right-clicking on element with {By.__name__}.{by_method}: {selector_value}")
            ActionChains(self.driver).context_click(element).perform()
            return True
        return False
    
    @retry
    def hover(self, selector, selector_type=None, timeout=None):
        """
        Hover over an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if hover successful, False otherwise
        """
        from selenium.webdriver.common.action_chains import ActionChains
        
        element = self.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.info(f"Hovering over element with {By.__name__}.{by_method}: {selector_value}")
            ActionChains(self.driver).move_to_element(element).perform()
            return True
        return False
    
    @retry
    def drag_and_drop(self, source_selector, target_selector, source_type=None, target_type=None):
        """
        Drag an element and drop it onto another element
        
        Args:
            source_selector: The selector string for the source element
            target_selector: The selector string for the target element
            source_type: Optional explicit selector type for source
            target_type: Optional explicit selector type for target
        
        Returns:
            True if drag and drop successful, False otherwise
        """
        from selenium.webdriver.common.action_chains import ActionChains
        
        source = self.find(source_selector, source_type)
        target = self.find(target_selector, target_type)
        
        if source and target:
            source_by, source_value = self._parse_selector(source_selector, source_type)
            target_by, target_value = self._parse_selector(target_selector, target_type)
            
            logger.info(f"Dragging element from {source_by}:{source_value} to {target_by}:{target_value}")
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            return True
        return False
    
    @retry
    def get_text(self, selector, selector_type=None, timeout=None):
        """
        Get the text content of an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            Text content or None if element not found after all retries
        
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.find(selector, selector_type, timeout)
        if element:
            text = element.text
            logger.info(f"Got text from element: {text}")
            return text
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for get_text: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def get_attribute(self, selector, attribute, selector_type=None, timeout=None):
        """
        Get an attribute value from an element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            attribute: The attribute name to get
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            Attribute value or None if element not found after all retries
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.find(selector, selector_type, timeout)
        if element:
            value = element.get_attribute(attribute)
            logger.info(f"Got attribute '{attribute}' from element: {value}")
            return value
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for get_attribute: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def is_displayed(self, selector, selector_type=None, timeout=None):
        """
        Check if an element is displayed
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is displayed, False otherwise
        """
        element = self.find(selector, selector_type, timeout)
        if element:
            result = element.is_displayed()
            logger.info(f"Element is displayed: {result}")
            return result
        return False
    
    @retry
    def is_enabled(self, selector, selector_type=None, timeout=None):
        """
        Check if an element is enabled
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is enabled, False otherwise
        """
        element = self.find(selector, selector_type, timeout)
        if element:
            result = element.is_enabled()
            logger.info(f"Element is enabled: {result}")
            return result
        return False
    
    def exists(self, selector, selector_type=None, timeout=0):
        """
        Check if an element exists in the DOM
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds (default is 0 for immediate check)
        
        Returns:
            True if element exists, False otherwise
        """
        element = self.find(selector, selector_type, timeout)
        result = element is not None
        logger.info(f"Element exists: {result}")
        return result