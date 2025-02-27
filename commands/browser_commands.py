"""
Browser-related commands for the testing framework
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.logger import Logger
from utils.helpers import take_screenshot

logger = Logger(__name__)

class BrowserCommands:
    def __init__(self, config):
        self.config = config
        self.driver = None
    
    def start(self, browser_type=None):
        """
        Start a browser session
        """
        browser = browser_type or self.config.DEFAULT_BROWSER
        logger.info(f"Starting {browser} browser")
        
        if browser.lower() == "chrome":
            options = ChromeOptions()
            if self.config.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if self.config.HEADLESS:
                options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
        elif browser.lower() == "edge":
            options = EdgeOptions()
            if self.config.HEADLESS:
                options.add_argument("--headless")
            self.driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser type: {browser}")
        
        # Set timeouts
        self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        self.driver.maximize_window()
        
        return self.driver
    
    def stop(self):
        """
        Stop the browser session
        """
        if self.driver:
            logger.info("Stopping browser")
            self.driver.quit()
            self.driver = None
    
    def visit(self, url):
        """
        Navigate to a URL
        """
        logger.info(f"Navigating to {url}")
        self.driver.get(url)
        return self.driver.current_url
    
    
    def refresh(self):
        """
        Refresh the current page
        """
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def back(self):
        """
        Navigate back to the previous page
        """
        logger.info("Going back")
        self.driver.back()
    
    def forward(self):
        """
        Navigate forward to the next page
        """
        logger.info("Going forward")
        self.driver.forward()
    
    def get_title(self):
        """
        Get the title of the current page
        """
        return self.driver.title
    
    def get_url(self):
        """
        Get the URL of the current page
        """
        return self.driver.current_url
    
    def screenshot(self, name=None):
        """
        Take a screenshot of the current page
        """
        filename = take_screenshot(self.driver, name)
        logger.info(f"Screenshot saved: {filename}")
        return filename
    
    def execute_script(self, script, *args):
        """
        Execute JavaScript in the browser
        """
        return self.driver.execute_script(script, *args)
    
    def set_window_size(self, width, height):
        """
        Set the window size
        """
        logger.info(f"Setting window size to {width}x{height}")
        self.driver.set_window_size(width, height)
    
    def switch_to_frame(self, frame_reference):
        """
        Switch to a frame by index, name, or element
        """
        logger.info(f"Switching to frame: {frame_reference}")
        self.driver.switch_to.frame(frame_reference)
    
    def switch_to_default_content(self):
        """
        Switch back to the main document
        """
        logger.info("Switching to default content")
        self.driver.switch_to.default_content()
