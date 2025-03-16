import time

def _login(runner, url, username, password):
    """
    Test login functionality using dynamic selectors
    """
    # Navigate to the demo site
    runner.browser.get(url)
    
    # Using ID selectors (prefix #)
    runner.forms.type("#username", username)
    runner.forms.type("#password", password)
    
    # Using CSS selector (default)
    runner.elements.click("button[type='submit']")
    
    # Using class selector (prefix .)
    runner.wait.wait_for_element_present(".flash.success")
    
    # Validate success message
    assert runner.validation.assert_text_contains(".flash.success", "You logged into a secure area") == True, "Login success message not found"
    
    # Validate URL
    assert runner.validation.assert_url_contains("/secure") == True, "URL does not contain /secure"
    
    # Using XPath (prefix //)
    runner.elements.click("//a[@href='/logout']")
    
    # Verify logout
    assert runner.validation.assert_url_contains("/login") == True, "URL does not contain /login after logout"

def _form_interactions(runner, formPage, checkboxesPage):
    """
    Test form interactions using dynamic selectors
    """
    # Navigate to the form page
    runner.browser.get(formPage)
    
    # Use dynamic selectors for dropdown
    runner.forms.select_by_text("#dropdown", "Option 1")
    assert runner.forms.get_selected_option_value("#dropdown") == "1", "Selected option value is not 1"
    
    # Navigate to checkboxes page
    runner.browser.get(checkboxesPage)
    
    # Find and interact with checkboxes using XPath
    checkboxes = runner.elements.find_all("//input[@type='checkbox']")
    
    # Check first checkbox if not already checked
    if not runner.forms.is_checked("(//input[@type='checkbox'])[1]"):
        runner.elements.click("(//input[@type='checkbox'])[1]")
    
    # Verify both checkboxes are checked
    assert runner.forms.is_checked("(//input[@type='checkbox'])[1]") == True, "First checkbox is not checked"
    assert runner.forms.is_checked("(//input[@type='checkbox'])[2]") == True, "Second checkbox is not checked"

def _multiple_selector_types(runner, loginPage, username, password):
    """
    Test using multiple selector types in one test
    """
    # Navigate to the login page
    runner.browser.get(loginPage)
    
    # ID selector - clear and type text
    runner.forms.clear("#username")
    runner.forms.type("#username", username)
    
    # Name selector - typically used with forms
    # Note: This site doesn't use name attributes, but this shows the syntax
    # runner.forms.type("@password", "SuperSecretPassword!")
    
    # Instead, using ID selector
    runner.forms.type("#password", password)
    
    # CSS selector (default) - click button
    runner.elements.click("button.radius")
    
    # XPath selector - verify element exists
    assert runner.validation.assert_element_exists("//h4[contains(text(), 'Welcome')]") == True, "Welcome header not found"
    
    # Link text selector - click logout link
    runner.elements.click("link=Logout")
    
    # Partial link text selector - alternative way to click links
    # runner.elements.click("partial-link=Log")
    
    # Class selector - check if element is present
    assert runner.elements.exists(".large-4") == True, "Element with class large-4 not found"

def _dynamic_waits(runner, loadingPage):
    """
    Test using dynamic selectors with wait commands
    """
    # Navigate to a page with dynamic elements
    runner.browser.get(loadingPage)
    
    # Click the start button using CSS selector
    runner.elements.click("div#start button")
    
    # Wait for loading indicator to disappear using XPath
    runner.wait.wait_for_element_invisible("//div[@id='loading']", timeout=1)
    
    # # Wait for text to appear using ID selector
    # runner.wait.wait_for_element_visible("#finish")
    
    # Verify the text using class selector
    assert runner.validation.assert_text_contains("#finish", "Hello World") == True, "Text 'Hello World' not found in #finish element"

def _table_interaction(runner, tablePage):
    """
    Test interacting with tables using dynamic selectors
    """
    # Navigate to tables page
    runner.browser.get(tablePage)
    
    # Get all rows in the first table using CSS selector
    table_rows = runner.elements.find_all("table#table1 tbody tr")
    assert len(table_rows) > 0, "No rows found in the table"
    
    # Get specific cell using XPath
    cell_text = runner.elements.get_text("//table[@id='table1']//tr[1]/td[2]")
    assert cell_text is not None, "Cell text is None"
    assert cell_text != "", "Cell text is empty"
    
    # Click on a header to sort by it
    runner.elements.click("#table1 th:nth-child(1)")
    
    # Verify the table has been sorted by checking the first row
    first_row_after_sort = runner.elements.get_text("//table[@id='table1']//tr[1]/td[1]")
    assert first_row_after_sort is not None, "First row text is None after sorting"
    assert first_row_after_sort != "", "First row text is empty after sorting"

