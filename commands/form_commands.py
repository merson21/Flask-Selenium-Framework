"""
form-related commands with dynamic selector support
"""

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from utils.logger import Logger
from commands.element_commands import ElementCommands
from utils.helpers import retry

logger = Logger(__name__)

class FormCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.element_commands = ElementCommands(driver, config)
    
    @retry
    def type(self, selector, text, selector_type=None, clear_first=True, timeout=None):
        """
        Type text into an input field
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The text to type
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            clear_first: Whether to clear the field before typing
            timeout: Optional timeout in seconds
        
        Returns:
            True if typing successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        
        if element:
            if clear_first:
                element.clear()
            
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Typing '{text}' into element with {by_method}: {selector_value}")
            element.send_keys(text)
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for type: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def clear(self, selector, selector_type=None, timeout=None):
        """
        Clear an input field
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if clearing successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Clearing element with {by_method}: {selector_value}")
            element.clear()
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for clear: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def submit(self, selector, selector_type=None, timeout=None):
        """
        Submit a form
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if submit successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Submitting form with {by_method}: {selector_value}")
            element.submit()
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for submit: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def select_by_text(self, selector, text, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by visible text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The visible text of the option to select
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option with text '{text}' from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_visible_text(text)
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for select_by_text: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def select_by_value(self, selector, value, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by value
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            value: The value attribute of the option to select
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option with value '{value}' from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_value(value)
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for select_by_value: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def select_by_index(self, selector, index, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by index
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            index: The index of the option to select (0-based)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option with index {index} from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_index(index)
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for select_by_index: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def get_selected_option_text(self, selector, selector_type=None, timeout=None):
        """
        Get the text of the selected option in a dropdown
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The text of the selected option
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Getting selected option text from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            selected_option = select.first_selected_option
            text = selected_option.text
            logger.info(f"Selected option text: {text}")
            return text
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for get_selected_option_text: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def get_selected_option_value(self, selector, selector_type=None, timeout=None):
        """
        Get the value of the selected option in a dropdown
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            The value of the selected option
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Getting selected option value from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            selected_option = select.first_selected_option
            value = selected_option.get_attribute("value")
            logger.info(f"Selected option value: {value}")
            return value
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for get_selected_option_value: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def check(self, selector, selector_type=None, timeout=None):
        """
        Check a checkbox if it's not already checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is now checked
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            if not element.is_selected():
                logger.info(f"Checking checkbox with {by_method}: {selector_value}")
                element.click()
            else:
                logger.info(f"Checkbox with {by_method}: {selector_value} is already checked")
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for check: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def uncheck(self, selector, selector_type=None, timeout=None):
        """
        Uncheck a checkbox if it's checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is now unchecked
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            if element.is_selected():
                logger.info(f"Unchecking checkbox with {by_method}: {selector_value}")
                element.click()
            else:
                logger.info(f"Checkbox with {by_method}: {selector_value} is already unchecked")
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for uncheck: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def is_checked(self, selector, selector_type=None, timeout=None):
        """
        Check if a checkbox is checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is checked, False if it exists but is not checked
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            result = element.is_selected()
            logger.info(f"Checkbox with {by_method}: {selector_value} is checked: {result}")
            return result
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for is_checked: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")
    
    @retry
    def upload_file(self, selector, file_path, selector_type=None, timeout=None):
        """
        Upload a file using a file input element
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            file_path: The path to the file to upload
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if file upload successful
            
        Raises:
            NoSuchElementException: If element not found (will be caught by retry decorator)
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Uploading file '{file_path}' using input with {by_method}: {selector_value}")
            element.send_keys(file_path)
            return True
        else:
            # Raise an exception that the retry decorator will catch
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.warning(f"Element not found for upload_file: {by_method}:{selector_value}")
            raise NoSuchElementException(f"Element not found: {by_method}:{selector_value}")