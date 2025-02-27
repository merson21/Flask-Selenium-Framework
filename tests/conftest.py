"""
Configuration for pytest
"""

import pytest

@pytest.fixture(scope="function")
def selenium_runner():
    """
    Fixture to provide a TestRunner instance for pytest
    """
    from flask_selenium_framework.test_runner import TestRunner
    runner = TestRunner()
    runner.setup()
    
    yield runner
    
    runner.teardown()