"""
Custom exceptions for the Flask Selenium Framework
"""

class ElementTimeoutException(Exception):
    """
    Exception raised when an element is not found within the timeout period
    """
    def __init__(self, selector, selector_type, timeout, message=None):
        self.selector = selector
        self.selector_type = selector_type
        self.timeout = timeout
        self.message = message or f"Element not found after {timeout} seconds: {selector_type} '{selector}'"
        super().__init__(self.message) 