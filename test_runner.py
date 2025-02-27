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
        Run a single test function with real-time updates
        """
        test_name = test_function.__name__
        logger.info(f"Running test: {test_name}")
        
        self.results['total'] += 1
        result = {
            'name': test_name,
            'status': 'running',  # Set initial status to running
            'error': None
        }
        
        # Add the test to results immediately with running status
        self.results['tests'].append(result)
        
        try:
            test_function(self)
            self.results['passed'] += 1
            result['status'] = 'passed'
            logger.info(f"Test passed: {test_name}")
        except Exception as e:
            self.results['failed'] += 1
            error_message = str(e)
            error_traceback = traceback.format_exc()
            logger.error(f"Test failed: {test_name} - {error_message}\n{error_traceback}")
            
            result['status'] = 'failed'
            result['error'] = error_message
            
            if self.config.TAKE_SCREENSHOT_ON_FAILURE and hasattr(self, 'browser'):
                from .utils.helpers import take_screenshot
                screenshot_path = take_screenshot(self.browser, f"failure_{test_name}")
                logger.info(f"Failure screenshot saved: {screenshot_path}")
                result['screenshot'] = screenshot_path
        
        return result


    
    def run_test_file(self, test_file_path):
        """
        Run all tests in a test file
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
        
        # Run each test function
        self.setup()
        try:
            for test_function in test_functions:
                self.run_test(test_function)
        finally:
            self.teardown()
        
        return self.results
    
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

