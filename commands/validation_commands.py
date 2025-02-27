"""
Validation-related commands with dynamic selector support
"""

from utils.logger import Logger
from commands.element_commands import ElementCommands

logger = Logger(__name__)

class ValidationCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.element_commands = ElementCommands(driver, config)
    
    def assert_element_exists(self, selector, selector_type=None, timeout=None):
        """
        Assert that an element exists in the DOM
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element exists, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = element is not None
        logger.info(f"Assert element exists with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        return result
    
    def assert_element_visible(self, selector, selector_type=None, timeout=None):
        """
        Assert that an element is visible
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is visible, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = element is not None and element.is_displayed()
        logger.info(f"Assert element visible with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        return result
    
    def assert_element_not_visible(self, selector, selector_type=None, timeout=None):
        """
        Assert that an element is not visible
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if element is not visible, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = element is None or not element.is_displayed()
        logger.info(f"Assert element not visible with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        return result
    
    def assert_text(self, selector, expected_text, selector_type=None, timeout=None):
        """
        Assert that an element contains specific text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            expected_text: The exact text that the element should contain
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if text matches exactly, False otherwise
        """
        actual_text = self.element_commands.get_text(selector, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = actual_text == expected_text
        logger.info(f"Assert element text equals '{expected_text}' with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result and actual_text is not None:
            logger.info(f"Actual text was: '{actual_text}'")
        return result
    
    def assert_text_contains(self, selector, partial_text, selector_type=None, timeout=None):
        """
        Assert that an element contains partial text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            partial_text: The text that should be contained within the element
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if text is contained, False otherwise
        """
        actual_text = self.element_commands.get_text(selector, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = actual_text is not None and partial_text in actual_text
        logger.info(f"Assert element text contains '{partial_text}' with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result and actual_text is not None:
            logger.info(f"Actual text was: '{actual_text}'")
        return result
    
    def assert_attribute(self, selector, attribute, expected_value, selector_type=None, timeout=None):
        """
        Assert that an element has a specific attribute value
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            attribute: The attribute name to check
            expected_value: The expected value of the attribute
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if attribute matches expected value, False otherwise
        """
        actual_value = self.element_commands.get_attribute(selector, attribute, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = actual_value == expected_value
        logger.info(f"Assert element attribute '{attribute}' equals '{expected_value}' with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result and actual_value is not None:
            logger.info(f"Actual value was: '{actual_value}'")
        return result
    
    def assert_attribute_contains(self, selector, attribute, partial_value, selector_type=None, timeout=None):
        """
        Assert that an element's attribute contains a partial value
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            attribute: The attribute name to check
            partial_value: The value that should be contained in the attribute
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if attribute contains partial value, False otherwise
        """
        actual_value = self.element_commands.get_attribute(selector, attribute, selector_type, timeout)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = actual_value is not None and partial_value in actual_value
        logger.info(f"Assert element attribute '{attribute}' contains '{partial_value}' with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result and actual_value is not None:
            logger.info(f"Actual value was: '{actual_value}'")
        return result
    
    def assert_checked(self, selector, selector_type=None, timeout=None):
        """
        Assert that a checkbox is checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is checked, False otherwise
        """
        from .form_commands import FormCommands
        form_commands = FormCommands(self.driver, self.config)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = form_commands.is_checked(selector, selector_type, timeout)
        logger.info(f"Assert element is checked with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        return result
    
    def assert_not_checked(self, selector, selector_type=None, timeout=None):
        """
        Assert that a checkbox is not checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is not checked, False otherwise
        """
        from .form_commands import FormCommands
        form_commands = FormCommands(self.driver, self.config)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        result = not form_commands.is_checked(selector, selector_type, timeout)
        logger.info(f"Assert element is not checked with {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        return result
    
    def assert_url(self, expected_url):
        """
        Assert that the current URL matches the expected URL
        
        Args:
            expected_url: The URL that the browser should be at
        
        Returns:
            True if URL matches, False otherwise
        """
        actual_url = self.driver.current_url
        result = actual_url == expected_url
        logger.info(f"Assert URL equals '{expected_url}' - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual URL was: '{actual_url}'")
        return result
    
    def assert_url_contains(self, partial_url):
        """
        Assert that the current URL contains a partial URL
        
        Args:
            partial_url: The text that should be contained in the URL
        
        Returns:
            True if URL contains partial URL, False otherwise
        """
        actual_url = self.driver.current_url
        result = partial_url in actual_url
        logger.info(f"Assert URL contains '{partial_url}' - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual URL was: '{actual_url}'")
        return result
    
    def assert_title(self, expected_title):
        """
        Assert that the page title matches the expected title
        
        Args:
            expected_title: The title that the page should have
        
        Returns:
            True if title matches, False otherwise
        """
        actual_title = self.driver.title
        result = actual_title == expected_title
        logger.info(f"Assert title equals '{expected_title}' - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual title was: '{actual_title}'")
        return result
    
    def assert_title_contains(self, partial_title):
        """
        Assert that the page title contains a partial title
        
        Args:
            partial_title: The text that should be contained in the title
        
        Returns:
            True if title contains partial title, False otherwise
        """
        actual_title = self.driver.title
        result = partial_title in actual_title
        logger.info(f"Assert title contains '{partial_title}' - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual title was: '{actual_title}'")
        return result
    
    def assert_element_count(self, selector, expected_count, selector_type=None):
        """
        Assert that the number of elements matching a selector equals the expected count
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            expected_count: The expected number of matching elements
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
        
        Returns:
            True if count matches, False otherwise
        """
        elements = self.element_commands.find_all(selector, selector_type)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        actual_count = len(elements)
        result = actual_count == expected_count
        logger.info(f"Assert element count equals {expected_count} for {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual count was: {actual_count}")
        return result
    
    def assert_element_count_greater_than(self, selector, min_count, selector_type=None):
        """
        Assert that the number of elements matching a selector is greater than min_count
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            min_count: The minimum expected number of matching elements
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
        
        Returns:
            True if count is greater than min_count, False otherwise
        """
        elements = self.element_commands.find_all(selector, selector_type)
        by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
        actual_count = len(elements)
        result = actual_count > min_count
        logger.info(f"Assert element count greater than {min_count} for {by_method}: {selector_value} - {'PASS' if result else 'FAIL'}")
        if not result:
            logger.info(f"Actual count was: {actual_count}")
        return result