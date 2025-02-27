# Flask Selenium Framework Command Reference

This document details all available commands in the Flask Selenium Framework with examples using the new dynamic selector syntax.

## Selector Types

The framework now supports automatic detection of selector types based on the prefix:

| Prefix | Selector Type | Example | Description |
|--------|--------------|---------|-------------|
| `#` | ID | `#login-button` | Selects element by ID |
| `.` | Class Name | `.btn-primary` | Selects element by class name |
| `@` | Name | `@username` | Selects element by name attribute |
| `//` | XPath | `//div[@id='content']` | Selects element using XPath |
| `link=` | Link Text | `link=Click here` | Selects link with exact text |
| `partial-link=` | Partial Link Text | `partial-link=Click` | Selects link containing text |
| *(none)* | CSS Selector | `div.container > p` | Default: CSS selector |

## Browser Commands

### Navigation

```python
# Navigate to a URL
runner.browser.get("https://www.example.com")

# Refresh the current page
runner.browser.refresh()

# Navigate back to the previous page
runner.browser.back()

# Navigate forward to the next page
runner.browser.forward()
```

### Information

```python
# Get the title of the current page
title = runner.browser.get_title()

# Get the URL of the current page
url = runner.browser.get_url()
```

### Screenshots & JavaScript

```python
# Take a screenshot
runner.browser.screenshot("example")

# Execute JavaScript
runner.browser.execute_script("return document.title")
```

### Window & Frames

```python
# Set window size
runner.browser.set_window_size(1024, 768)

# Switch to a frame
runner.browser.switch_to_frame("#myframe")  # By ID
runner.browser.switch_to_frame(0)           # By index

# Switch back to main document
runner.browser.switch_to_default_content()
```

## Element Commands

### Finding Elements

```python
# Find an element using ID selector
element = runner.elements.find("#username")

# Find an element using class selector
element = runner.elements.find(".navbar")

# Find an element using CSS selector (default)
element = runner.elements.find("div.container > button")

# Find an element using XPath
element = runner.elements.find("//button[@type='submit']")

# Find an element using name attribute
element = runner.elements.find("@email")

# Find an element using link text
element = runner.elements.find("link=Click Here")

# Find an element using partial link text
element = runner.elements.find("partial-link=Click")

# Find all matching elements
elements = runner.elements.find_all(".product-item")

# Check if an element exists (returns immediately)
exists = runner.elements.exists("#notification", timeout=0)
```

### Element Interactions

```python
# Click an element
runner.elements.click("#submit-button")

# Double-click an element
runner.elements.double_click(".item")

# Right-click an element
runner.elements.right_click("#context-menu")

# Hover over an element
runner.elements.hover(".dropdown-toggle")

# Drag and drop elements
runner.elements.drag_and_drop("#source", "#target")
```

### Element Properties

```python
# Get element text
text = runner.elements.get_text(".message")

# Get element attribute
href = runner.elements.get_attribute("a.link", "href")

# Check if element is displayed
is_visible = runner.elements.is_displayed("#popup")

# Check if element is enabled
is_enabled = runner.elements.is_enabled("#submit-button")
```

## Form Commands

### Input Fields

```python
# Type text into an input field
runner.forms.type("#username", "testuser")
runner.forms.type("@email", "test@example.com")
runner.forms.type(".search-input", "search term")

# Clear an input field
runner.forms.clear("#search")

# Submit a form
runner.forms.submit("#login-form")
```

### Dropdowns

```python
# Select dropdown option by visible text
runner.forms.select_by_text("#country", "United States")

# Select dropdown option by value
runner.forms.select_by_value(".language-select", "en")

# Select dropdown option by index
runner.forms.select_by_index("#month", 0)  # First option

# Get selected option text
selected_text = runner.forms.get_selected_option_text("#country")

# Get selected option value
selected_value = runner.forms.get_selected_option_value("#country")
```

### Checkboxes & Radio Buttons

```python
# Check a checkbox
runner.forms.check("#terms")

# Uncheck a checkbox
runner.forms.uncheck("#newsletter")

# Check if a checkbox is checked
is_checked = runner.forms.is_checked(".consent-checkbox")
```

### File Upload

```python
# Upload a file
runner.forms.upload_file("#file-upload", "/path/to/file.jpg")
```

## Wait Commands

### Element Waits

```python
# Wait for element to be visible
runner.wait.wait_for_element_visible("#loading-indicator")

# Wait for element to be invisible
runner.wait.wait_for_element_invisible(".spinner")

# Wait for element to be present in DOM
runner.wait.wait_for_element_present("//div[@id='results']")

# Wait for element to be clickable
runner.wait.wait_for_element_clickable("#submit-button")

# Wait for element to contain text
runner.wait.wait_for_text(".alert", "Success")

# Wait for element to have attribute value
runner.wait.wait_for_attribute("#status", "data-state", "complete")

# Wait for element count
runner.wait.wait_for_elements_count(".item", 5)  # Exactly 5 items
runner.wait.wait_for_elements_count_greater_than(".result", 3)  # More than 3 results
```

### Page Waits

```python
# Wait for URL to match
runner.wait.wait_for_url("https://example.com/dashboard")

# Wait for URL to contain
runner.wait.wait_for_url_contains("/dashboard")

# Wait for page title to match
runner.wait.wait_for_title("Dashboard - Example")

# Wait for page title to contain
runner.wait.wait_for_title_contains("Dashboard")

# Wait for page to load completely
runner.wait.wait_for_page_load()

# Wait for AJAX requests to complete (jQuery)
runner.wait.wait_for_ajax()

# Wait for specific time (seconds)
runner.wait.wait(2)
```

## Validation Commands

### Element Assertions

```python
# Assert element exists
assert runner.validation.assert_element_exists("#welcome-message")

# Assert element is visible
assert runner.validation.assert_element_visible(".notification")

# Assert element is not visible
assert runner.validation.assert_element_not_visible("#error-message")

# Assert element text equals
assert runner.validation.assert_text("#title", "Welcome to Example")

# Assert element text contains
assert runner.validation.assert_text_contains(".alert", "successfully")

# Assert element attribute equals
assert runner.validation.assert_attribute("img.logo", "alt", "Company Logo")

# Assert element attribute contains
assert runner.validation.assert_attribute_contains("a.link", "href", "example.com")

# Assert element count
assert runner.validation.assert_element_count(".item", 5)  # Exactly 5 items
assert runner.validation.assert_element_count_greater_than(".result", 3)  # More than 3 results
```

### Form Assertions

```python
# Assert checkbox is checked
assert runner.validation.assert_checked("#terms")

# Assert checkbox is not checked
assert runner.validation.assert_not_checked("#newsletter")
```

### Page Assertions

```python
# Assert URL equals
assert runner.validation.assert_url("https://example.com/dashboard")

# Assert URL contains
assert runner.validation.assert_url_contains("/dashboard")

# Assert title equals
assert runner.validation.assert_title("Dashboard - Example")

# Assert title contains
assert runner.validation.assert_title_contains("Dashboard")
```

## Creating Custom Commands

You can create custom command classes that leverage the dynamic selector functionality:

```python
class CustomCommands:
    def __init__(self, runner):
        self.runner = runner
    
    def login(self, username, password, remember=False):
        """
        Custom command to perform login
        """
        # Navigate to login page
        self.runner.browser.get("https://example.com/login")
        
        # Fill login form using dynamic selectors
        self.runner.forms.type("#username", username)
        self.runner.forms.type("#password", password)
        
        # Check remember me if needed
        if remember:
            self.runner.forms.check("#remember")
        
        # Submit form
        self.runner.elements.click(".login-button")
        
        # Wait for dashboard
        return self.runner.wait.wait_for_url_contains("/dashboard")
```

## Best Practices

1. **Use Specific Selectors**: ID selectors (`#element-id`) are most reliable, followed by name attributes (`@name`).

2. **Leverage Auto-Detection**: The prefix-based auto-detection makes your code more readable.

3. **Defensive Waiting**: Always use appropriate waits for dynamic elements.

4. **Assertions as Return Values**: All validation commands return booleans, so use them with `assert`:
   ```python
   # Good
   assert runner.validation.assert_text("#message", "Success")
   
   # Not Recommended
   runner.validation.assert_text("#message", "Success")  # Result ignored
   ```

5. **Consistent Selector Strategy**: Decide on a selector strategy for your project and stick to it.

6. **Add Timeouts When Needed**: For long operations, specify explicit timeouts:
   ```python
   runner.wait.wait_for_element_visible("#slow-element", timeout=30)
   ```

7. **Keep Selectors Simple**: Avoid overly complex selectors that could break with minor UI changes.
