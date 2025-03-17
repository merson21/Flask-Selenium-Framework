"""
Example test demonstrating element timeout handling
"""

def test_element_timeout_example(runner):
    """
    This test demonstrates how element timeout exceptions are handled
    """
    loadingPage = "https://the-internet.herokuapp.com/dynamic_loading/1"
    # Navigate to a page with dynamic elements
    runner.browser.get(loadingPage)
    
    # Click the start button using CSS selector
    assert runner.elements.click("div#starts button", timeout=3), \
        "Button query selector not found"
    
    # Wait for loading indicator to disappear using XPath
    # This will fail the test if the element doesn't become invisible within 1 second
    assert runner.wait.wait_for_element_invisible("//div[@id='loading']", timeout=1), \
        "Loading indicator did not disappear within the timeout period"

def test_element_timeout_example2(runner):
    """
    This test demonstrates how element timeout exceptions are handled
    """
    loadingPage = "https://the-internet.herokuapp.com/dynamic_loading/1"
    # Navigate to a page with dynamic elements
    runner.browser.get(loadingPage)
    
    # Click the start button using CSS selector
    assert runner.elements.click("div#start button", timeout=3), \
        "Button query selector not found"
    
    # Wait for loading indicator to disappear using XPath
    # This will fail the test if the element doesn't become invisible within 1 second
    assert runner.wait.wait_for_element_invisible("//div[@id='loading']", timeout=1), \
        "Loading indicator did not disappear within the timeout period"


def test_element_timeout_example3(runner):
    """
    This test demonstrates how element timeout exceptions are handled
    """
    loadingPage = "https://the-internet.herokuapp.com/dynamic_loading/1"
    # Navigate to a page with dynamic elements
    runner.browser.get(loadingPage)
    
    # Click the start button using CSS selector
    assert runner.elements.click("div#start button", timeout=3), \
        "Button query selector not found"
    
    # Wait for loading indicator to disappear using XPath
    # This will fail the test if the element doesn't become invisible within 1 second
    assert runner.wait.wait_for_element_invisible("//div[@id='loadings']", timeout=1), \
        "Loading indicator did not disappear within the timeout period"
