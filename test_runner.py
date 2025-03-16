"""
Test runner for executing Selenium tests
"""

import sys
import os
import importlib
import inspect
import traceback
from utils.logger import Logger
from commands.browser_commands import BrowserCommands
from commands.element_commands import ElementCommands
from commands.form_commands import FormCommands
from commands.validation_commands import ValidationCommands
from commands.wait_commands import WaitCommands
from config import Config
from utils.exceptions import ElementTimeoutException

logger = Logger(__name__)

class TestRunner:
    def __init__(self, config=None):
        self.config = config or Config()
        self.browser = None
        self.elements = None
        self.forms = None
        self.validation = None
        self.wait = None
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'tests': []
        }
    
    def setup(self, browser_type=None):
        """
        Set up the test environment
        """
        logger.info("Setting up test environment")
        browser_commands = BrowserCommands(self.config)
        self.browser = browser_commands.start(browser_type)
        
        self.elements = ElementCommands(self.browser, self.config)
        self.forms = FormCommands(self.browser, self.config)
        self.validation = ValidationCommands(self.browser, self.config)
        self.wait = WaitCommands(self.browser, self.config)
    
    def teardown(self):
        """
        Tear down the test environment
        """
        logger.info("Tearing down test environment")
        if hasattr(self, 'browser') and self.browser:
            BrowserCommands(self.config).stop()
    
    def run_test(self, test_function):
        """
        Run a single test function
        
        Args:
            test_function: The test function to run
            
        Returns:
            Dictionary with test results
        """
        test_name = test_function.__name__
        logger.info(f"Running test: {test_name}")
        
        result = {
            'name': test_name,
            'status': 'passed',
            'error': None,
            'screenshot': None
        }
        
        try:
            # Call the test function with self as argument
            test_function(self)
            
            self.results['passed'] += 1
            logger.info(f"Test passed: {test_name}")
            
            if self.config.TAKE_SCREENSHOT_ON_SUCCESS and hasattr(self, 'browser'):
                from utils.helpers import take_screenshot
                screenshot_path = take_screenshot(self.browser, f"success_{test_name}")
                logger.info(f"Success screenshot saved: {screenshot_path}")
                # Store just the filename without the 'screenshots/' prefix
                if screenshot_path.startswith('screenshots/'):
                    result['screenshot'] = screenshot_path.replace('screenshots/', '')
                else:
                    result['screenshot'] = screenshot_path
        except ElementTimeoutException as e:
            self.results['failed'] += 1
            error_message = str(e)
            error_traceback = traceback.format_exc()
            logger.error(f"Test failed due to element timeout: {test_name} - {error_message}\n{error_traceback}")
            
            result['status'] = 'failed'
            result['error'] = error_message
            result['error_type'] = 'element_timeout'
            result['selector'] = e.selector
            result['selector_type'] = e.selector_type
            result['timeout'] = e.timeout
            
            if self.config.TAKE_SCREENSHOT_ON_FAILURE and hasattr(self, 'browser'):
                from utils.helpers import take_screenshot
                screenshot_path = take_screenshot(self.browser, f"failure_{test_name}")
                logger.error(f"Failure screenshot saved: {screenshot_path}")
                # Store just the filename without the 'screenshots/' prefix
                if screenshot_path.startswith('screenshots/'):
                    result['screenshot'] = screenshot_path.replace('screenshots/', '')
                else:
                    result['screenshot'] = screenshot_path
        except Exception as e:
            self.results['failed'] += 1
            error_message = str(e)
            error_traceback = traceback.format_exc()
            logger.error(f"Test failed: {test_name} - {error_message}\n{error_traceback}")
            
            result['status'] = 'failed'
            result['error'] = error_message
            
            if self.config.TAKE_SCREENSHOT_ON_FAILURE and hasattr(self, 'browser'):
                from utils.helpers import take_screenshot
                screenshot_path = take_screenshot(self.browser, f"failure_{test_name}")
                logger.error(f"Failure screenshot saved: {screenshot_path}")
                # Store just the filename without the 'screenshots/' prefix
                if screenshot_path.startswith('screenshots/'):
                    result['screenshot'] = screenshot_path.replace('screenshots/', '')
                else:
                    result['screenshot'] = screenshot_path
        
        return result


    
    def run_test_file(self, test_file_path):
        """
        Run all tests in a test file, continuing even if some tests fail
        """
        logger.info(f"Running tests from file: {test_file_path}")
        
        # Import the test module
        module_name = os.path.basename(test_file_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, test_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find all test functions
        test_functions = []
        for name, obj in inspect.getmembers(module):
            if name.startswith('test_') and callable(obj):
                test_functions.append(obj)
        
        # Setup the environment once for all tests
        self.setup()
        
        results = {
            'total': len(test_functions),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'tests': []
        }
        
        try:
            # Run each test function, continuing even if some fail
            for func in test_functions:
                try:
                    result = self.run_test(func)
                    results['tests'].append(result)
                    
                    # Update counters
                    if result['status'] == 'passed':
                        results['passed'] += 1
                    elif result['status'] == 'failed':
                        results['failed'] += 1
                    else:
                        results['skipped'] += 1
                except Exception as e:
                    # If run_test itself throws an exception, log it but continue
                    logger.error(f"Error running test {func.__name__}: {str(e)}")
                    results['failed'] += 1
                    results['tests'].append({
                        'name': func.__name__,
                        'status': 'failed',
                        'error': str(e)
                    })
        finally:
            # Always clean up
            self.teardown()
        
        return results
        
    def run_test_directory(self, directory_path):
        """
        Run all tests in a directory
        """
        logger.info(f"Running tests from directory: {directory_path}")
        
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'tests': []
        }
        
        # Find all test files
        test_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(os.path.join(root, file))
        
        # Run each test file
        for test_file in test_files:
            file_results = self.run_test_file(test_file)
            results['total'] += file_results['total']
            results['passed'] += file_results['passed']
            results['failed'] += file_results['failed']
            results['skipped'] += file_results['skipped']
            results['tests'].extend(file_results['tests'])
        
        return results
    
    def print_results(self):
        """
        Print the test results
        """
        logger.info("\n=== Test Results ===")
        logger.info(f"Total tests: {self.results['total']}")
        logger.info(f"Passed: {self.results['passed']}")
        logger.info(f"Failed: {self.results['failed']}")
        logger.info(f"Skipped: {self.results['skipped']}")
        
        if self.results['failed'] > 0:
            logger.info("\nFailed tests:")
            for test in self.results['tests']:
                if test['status'] == 'failed':
                    logger.info(f"- {test['name']}: {test['error']}")
        
        return self.results

