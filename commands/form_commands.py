"""
form-related commands with dynamic selector support
"""

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from utils.logger import Logger
from commands.element_commands import ElementCommands

logger = Logger(__name__)

class FormCommands:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.element_commands = ElementCommands(driver, config)
    
    def type(self, selector, text, selector_type=None, clear_first=True, timeout=None, raise_exception=False):
        """
        Type text into an input field
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The text to type
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            clear_first: Whether to clear the field before typing
            timeout: Optional timeout in seconds
            raise_exception: Whether to raise an exception if element not found
        
        Returns:
            True if typing successful, False otherwise
        
        Raises:
            ElementTimeoutException: If raise_exception is True and element not found
        """
        try:
            if raise_exception:
                element = self.element_commands.find_or_fail(selector, selector_type, timeout)
            else:
                element = self.element_commands.find(selector, selector_type, timeout)
            
            if element:
                if clear_first:
                    element.clear()
                
                by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
                logger.info(f"Typing '{text}' into element with {by_method}: {selector_value}")
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            if raise_exception:
                raise
            logger.error(f"Error typing into element: {str(e)}")
            return False
    
    def clear(self, selector, selector_type=None, timeout=None):
        """
        Clear the content of an input field
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if clearing successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Clearing text from element with {by_method}: {selector_value}")
            element.clear()
            return True
        return False
    
    def submit(self, selector, selector_type=None, timeout=None):
        """
        Submit a form
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if submit successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Submitting form with {by_method}: {selector_value}")
            element.submit()
            return True
        return False
    
    def select_by_text(self, selector, text, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by visible text
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            text: The visible text of the option to select
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option '{text}' from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_visible_text(text)
            return True
        return False
    
    def select_by_value(self, selector, value, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by value
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            value: The value attribute of the option to select
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option with value '{value}' from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_value(value)
            return True
        return False
    
    def select_by_index(self, selector, index, selector_type=None, timeout=None):
        """
        Select an option from a dropdown by index
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            index: The index of the option to select (0-based)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if selection successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Selecting option at index {index} from dropdown with {by_method}: {selector_value}")
            select = Select(element)
            select.select_by_index(index)
            return True
        return False
    
    def get_selected_option_text(self, selector, selector_type=None, timeout=None):
        """
        Get the text of the selected option in a dropdown
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            Text of the selected option or None if not found
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            select = Select(element)
            selected = select.first_selected_option
            text = selected.text
            logger.info(f"Selected option text: {text}")
            return text
        return None
    
    def get_selected_option_value(self, selector, selector_type=None, timeout=None):
        """
        Get the value of the selected option in a dropdown
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            Value of the selected option or None if not found
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            select = Select(element)
            selected = select.first_selected_option
            value = selected.get_attribute("value")
            logger.info(f"Selected option value: {value}")
            return value
        return None
    
    def check(self, selector, selector_type=None, timeout=None):
        """
        Check a checkbox
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if check successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            if not element.is_selected():
                by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
                logger.info(f"Checking checkbox with {by_method}: {selector_value}")
                element.click()
            else:
                by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
                logger.info(f"Checkbox with {by_method}: {selector_value} already checked")
            return True
        return False
    
    def uncheck(self, selector, selector_type=None, timeout=None):
        """
        Uncheck a checkbox
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if uncheck successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            if element.is_selected():
                by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
                logger.info(f"Unchecking checkbox with {by_method}: {selector_value}")
                element.click()
            else:
                by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
                logger.info(f"Checkbox with {by_method}: {selector_value} already unchecked")
            return True
        return False
    
    def is_checked(self, selector, selector_type=None, timeout=None):
        """
        Check if a checkbox is checked
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if checkbox is checked, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            result = element.is_selected()
            logger.info(f"Checkbox is checked: {result}")
            return result
        return False
    
    def upload_file(self, selector, file_path, selector_type=None, timeout=None):
        """
        Upload a file using a file input
        
        Args:
            selector: The selector string (can include prefix for auto-detection)
            file_path: Full path to the file to upload
            selector_type: Optional explicit selector type. If provided, overrides auto-detection.
            timeout: Optional timeout in seconds
        
        Returns:
            True if upload successful, False otherwise
        """
        element = self.element_commands.find(selector, selector_type, timeout)
        if element:
            by_method, selector_value = self.element_commands._parse_selector(selector, selector_type)
            logger.info(f"Uploading file: {file_path} to input with {by_method}: {selector_value}")
            element.send_keys(file_path)
            return True
        return False