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
    assert runner.elements.click("div#starts button"), \
        "Button query selector not found"
    
    # Wait for loading indicator to disappear using XPath
    # This will fail the test if the element doesn't become invisible within 1 second
    assert runner.wait.wait_for_element_invisible("//div[@id='loading']", timeout=1), \
        "Loading indicator did not disappear within the timeout period"

    # Navigate to a test page
    # runner.browser.get("https://the-internet.herokuapp.com/")
    #     # Try to find an element that doesn't exist with default behavior (returns None)
    # # non_existent = runner.elements.find("#non-existent-element", timeout=3)
    # # if non_existent is None:
    # #     runner.browser.execute_script("console.log('Element not found, continuing test')")
    
    # # Try to find an element that doesn't exist with exception raising
    # try:
    #     runner.elements.find_or_fail("#another-non-existent-element", timeout=1)
    # except Exception as e:
    #     runner.browser.execute_script(f"console.log('Caught exception: {str(e)}')")
    
    # This will raise an ElementTimeoutException that will be caught by the test runner
    # and displayed with detailed information in the UI
    # runner.elements.find_or_fail("#this-will-fail-the-test", timeout=3)
    
    # This line will never be reached
    # runner.browser.execute_script("console.log('This should not be executed')") 
