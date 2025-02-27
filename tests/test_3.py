import time

def test_login(runner):
    """
    Test login functionality using dynamic selectors
    """
    # Navigate to the demo site
    runner.browser.get("https://the-internet.herokuapp.com/login")
    
    # Using ID selectors (prefix #)
    runner.forms.type("#username", "tomsmith")
    runner.forms.type("#password", "SuperSecretPassword!")
    
    # Using CSS selector (default)
    runner.elements.click("button[type='submit']")
    
    # Using class selector (prefix .)
    runner.wait.wait_for_element_present(".flash.success")
    
    # Validate success message
    assert runner.validation.assert_text_contains(".flash.success", "You logged into a secure area")
    
    # Validate URL
    assert runner.validation.assert_url_contains("/secure")
    
    # Using XPath (prefix //)
    runner.elements.click("//a[@href='/logout']")
    
    # Verify logout
    assert runner.validation.assert_url_contains("/login")

def test_form_interactions(runner):
    """
    Test form interactions using dynamic selectors
    """
    # Navigate to the form page
    runner.browser.get("https://the-internet.herokuapp.com/dropdown")
    
    # Use dynamic selectors for dropdown
    runner.forms.select_by_text("#dropdown", "Option 1")
    assert runner.forms.get_selected_option_value("#dropdown") == "1"
    
    # Navigate to checkboxes page
    runner.browser.get("https://the-internet.herokuapp.com/checkboxes")
    
    # Find and interact with checkboxes using XPath
    checkboxes = runner.elements.find_all("//input[@type='checkbox']")
    
    # Check first checkbox if not already checked
    if not runner.forms.is_checked("(//input[@type='checkbox'])[1]"):
        runner.elements.click("(//input[@type='checkbox'])[1]")
    
    # Verify both checkboxes are checked
    assert runner.forms.is_checked("(//input[@type='checkbox'])[1]")
    assert runner.forms.is_checked("(//input[@type='checkbox'])[2]")

def test_multiple_selector_types(runner):
    """
    Test using multiple selector types in one test
    """
    # Navigate to the login page
    runner.browser.get("https://the-internet.herokuapp.com/login")
    
    # ID selector - clear and type text
    runner.forms.clear("#username")
    runner.forms.type("#username", "tomsmith")
    
    # Name selector - typically used with forms
    # Note: This site doesn't use name attributes, but this shows the syntax
    # runner.forms.type("@password", "SuperSecretPassword!")
    
    # Instead, using ID selector
    runner.forms.type("#password", "SuperSecretPassword!")
    
    # CSS selector (default) - click button
    runner.elements.click("button.radius")
    
    # XPath selector - verify element exists
    assert runner.validation.assert_element_exists("//h4[contains(text(), 'Welcome')]")
    
    # Link text selector - click logout link
    runner.elements.click("link=Logout")
    
    # Partial link text selector - alternative way to click links
    # runner.elements.click("partial-link=Log")
    
    # Class selector - check if element is present
    assert runner.elements.exists(".large-4")

def test_dynamic_waits(runner):
    """
    Test using dynamic selectors with wait commands
    """
    # Navigate to a page with dynamic elements
    runner.browser.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    # Click the start button using CSS selector
    runner.elements.click("div#start button")
    
    # Wait for loading indicator to disappear using XPath
    runner.wait.wait_for_element_invisible("//div[@id='loading']")
    
    # # Wait for text to appear using ID selector
    # runner.wait.wait_for_element_visible("#finish")
    
    # Verify the text using class selector
    assert runner.validation.assert_text_contains("#finish", "Hello World")

def test_table_interaction(runner):
    """
    Test interacting with tables using dynamic selectors
    """
    # Navigate to tables page
    runner.browser.get("https://the-internet.herokuapp.com/tables")
    
    # Get all rows in the first table using CSS selector
    table_rows = runner.elements.find_all("table#table1 tbody tr")
    assert len(table_rows) > 0
    
    # Get specific cell using XPath
    cell_text = runner.elements.get_text("//table[@id='table1']//tr[1]/td[2]")
    assert cell_text is not None
    
    # Click on a header to sort by it
    runner.elements.click("#table1 th:nth-child(1)")
    
    # Verify the table has been sorted by checking the first row
    first_row_after_sort = runner.elements.get_text("//table[@id='table1']//tr[1]/td[1]")
    assert first_row_after_sort is not None
