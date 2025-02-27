# Flask Selenium Framework - Complete Command Reference

This document provides a comprehensive listing of all available commands in the Flask Selenium Framework, organized by category.

## Dynamic Selector Prefixes

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

| Command | Description | Example |
|---------|-------------|---------|
| `browser.get(url)` | Navigate to a URL | `runner.browser.get("https://example.com")` |
| `browser.refresh()` | Refresh the current page | `runner.browser.refresh()` |
| `browser.back()` | Navigate back to the previous page | `runner.browser.back()` |
| `browser.forward()` | Navigate forward to the next page | `runner.browser.forward()` |
| `browser.get_title()` | Get the title of the current page | `title = runner.browser.get_title()` |
| `browser.get_url()` | Get the URL of the current page | `url = runner.browser.get_url()` |
| `browser.screenshot(name)` | Take a screenshot | `runner.browser.screenshot("homepage")` |
| `browser.execute_script(script, *args)` | Execute JavaScript | `runner.browser.execute_script("return document.title")` |
| `browser.set_window_size(width, height)` | Set the window size | `runner.browser.set_window_size(1024, 768)` |
| `browser.switch_to_frame(frame_reference)` | Switch to a frame | `runner.browser.switch_to_frame("#myframe")` |
| `browser.switch_to_default_content()` | Switch back to main document | `runner.browser.switch_to_default_content()` |

## Element Commands

| Command | Description | Example |
|---------|-------------|---------|
| `elements.find(selector, selector_type=None, timeout=None)` | Find an element | `element = runner.elements.find("#username")` |
| `elements.find_all(selector, selector_type=None)` | Find all matching elements | `elements = runner.elements.find_all(".product-item")` |
| `elements.click(selector, selector_type=None, timeout=None)` | Click an element | `runner.elements.click("#submit-button")` |
| `elements.double_click(selector, selector_type=None, timeout=None)` | Double-click an element | `runner.elements.double_click(".item")` |
| `elements.right_click(selector, selector_type=None, timeout=None)` | Right-click an element | `runner.elements.right_click("#context-menu")` |
| `elements.hover(selector, selector_type=None, timeout=None)` | Hover over an element | `runner.elements.hover(".dropdown-toggle")` |
| `elements.drag_and_drop(source_selector, target_selector, source_type=None, target_type=None)` | Drag and drop elements | `runner.elements.drag_and_drop("#source", "#target")` |
| `elements.get_text(selector, selector_type=None, timeout=None)` | Get element text | `text = runner.elements.get_text(".message")` |
| `elements.get_attribute(selector, attribute, selector_type=None, timeout=None)` | Get element attribute | `href = runner.elements.get_attribute("a.link", "href")` |
| `elements.is_displayed(selector, selector_type=None, timeout=None)` | Check if element is displayed | `is_visible = runner.elements.is_displayed("#popup")` |
| `elements.is_enabled(selector, selector_type=None, timeout=None)` | Check if element is enabled | `is_enabled = runner.elements.is_enabled("#submit-button")` |
| `elements.exists(selector, selector_type=None, timeout=0)` | Check if element exists | `exists = runner.elements.exists("#notification")` |

## Form Commands

| Command | Description | Example |
|---------|-------------|---------|
| `forms.type(selector, text, selector_type=None, clear_first=True, timeout=None)` | Type text into an input field | `runner.forms.type("#username", "testuser")` |
| `forms.clear(selector, selector_type=None, timeout=None)` | Clear an input field | `runner.forms.clear("#search")` |
| `forms.submit(selector, selector_type=None, timeout=None)` | Submit a form | `runner.forms.submit("#login-form")` |
| `forms.select_by_text(selector, text, selector_type=None, timeout=None)` | Select dropdown option by visible text | `runner.forms.select_by_text("#country", "United States")` |
| `forms.select_by_value(selector, value, selector_type=None, timeout=None)` | Select dropdown option by value | `runner.forms.select_by_value(".language-select", "en")` |
| `forms.select_by_index(selector, index, selector_type=None, timeout=None)` | Select dropdown option by index | `runner.forms.select_by_index("#month", 0)` |
| `forms.get_selected_option_text(selector, selector_type=None, timeout=None)` | Get selected option text | `selected_text = runner.forms.get_selected_option_text("#country")` |
| `forms.get_selected_option_value(selector, selector_type=None, timeout=None)` | Get selected option value | `selected_value = runner.forms.get_selected_option_value("#country")` |
| `forms.check(selector, selector_type=None, timeout=None)` | Check a checkbox | `runner.forms.check("#terms")` |
| `forms.uncheck(selector, selector_type=None, timeout=None)` | Uncheck a checkbox | `runner.forms.uncheck("#newsletter")` |
| `forms.is_checked(selector, selector_type=None, timeout=None)` | Check if a checkbox is checked | `is_checked = runner.forms.is_checked(".consent-checkbox")` |
| `forms.upload_file(selector, file_path, selector_type=None, timeout=None)` | Upload a file | `runner.forms.upload_file("#file-upload", "/path/to/file.jpg")` |

## Wait Commands

| Command | Description | Example |
|---------|-------------|---------|
| `wait.wait_for_element_visible(selector, selector_type=None, timeout=None)` | Wait for element to be visible | `runner.wait.wait_for_element_visible("#loading-indicator")` |
| `wait.wait_for_element_invisible(selector, selector_type=None, timeout=None)` | Wait for element to be invisible | `runner.wait.wait_for_element_invisible(".spinner")` |
| `wait.wait_for_element_present(selector, selector_type=None, timeout=None)` | Wait for element to be present in DOM | `runner.wait.wait_for_element_present("//div[@id='results']")` |
| `wait.wait_for_element_clickable(selector, selector_type=None, timeout=None)` | Wait for element to be clickable | `runner.wait.wait_for_element_clickable("#submit-button")` |
| `wait.wait_for_text(selector, text, selector_type=None, timeout=None)` | Wait for element to contain text | `runner.wait.wait_for_text(".alert", "Success")` |
| `wait.wait_for_attribute(selector, attribute, value, selector_type=None, timeout=None)` | Wait for element to have attribute value | `runner.wait.wait_for_attribute("#status", "data-state", "complete")` |
| `wait.wait_for_url(url, timeout=None)` | Wait for URL to match | `runner.wait.wait_for_url("https://example.com/dashboard")` |
| `wait.wait_for_url_contains(partial_url, timeout=None)` | Wait for URL to contain | `runner.wait.wait_for_url_contains("/dashboard")` |
| `wait.wait_for_title(title, timeout=None)` | Wait for page title to match | `runner.wait.wait_for_title("Dashboard - Example")` |
| `wait.wait_for_title_contains(partial_title, timeout=None)` | Wait for page title to contain | `runner.wait.wait_for_title_contains("Dashboard")` |
| `wait.wait(seconds)` | Wait for specific time in seconds | `runner.wait.wait(2)` |
| `wait.wait_for_elements_count(selector, count, selector_type=None, timeout=None)` | Wait for element count to equal | `runner.wait.wait_for_elements_count(".item", 5)` |
| `wait.wait_for_elements_count_greater_than(selector, min_count, selector_type=None, timeout=None)` | Wait for element count to be greater than | `runner.wait.wait_for_elements_count_greater_than(".result", 3)` |
| `wait.wait_for_page_load(timeout=None)` | Wait for page to load completely | `runner.wait.wait_for_page_load()` |
| `wait.wait_for_ajax(timeout=None)` | Wait for AJAX requests to complete | `runner.wait.wait_for_ajax()` |

## Validation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `validation.assert_element_exists(selector, selector_type=None, timeout=None)` | Assert element exists | `assert runner.validation.assert_element_exists("#welcome-message")` |
| `validation.assert_element_visible(selector, selector_type=None, timeout=None)` | Assert element is visible | `assert runner.validation.assert_element_visible(".notification")` |
| `validation.assert_element_not_visible(selector, selector_type=None, timeout=None)` | Assert element is not visible | `assert runner.validation.assert_element_not_visible("#error-message")` |
| `validation.assert_text(selector, expected_text, selector_type=None, timeout=None)` | Assert element text equals | `assert runner.validation.assert_text("#title", "Welcome to Example")` |
| `validation.assert_text_contains(selector, partial_text, selector_type=None, timeout=None)` | Assert element text contains | `assert runner.validation.assert_text_contains(".alert", "successfully")` |
| `validation.assert_attribute(selector, attribute, expected_value, selector_type=None, timeout=None)` | Assert element attribute equals | `assert runner.validation.assert_attribute("img.logo", "alt", "Company Logo")` |
| `validation.assert_attribute_contains(selector, attribute, partial_value, selector_type=None, timeout=None)` | Assert element attribute contains | `assert runner.validation.assert_attribute_contains("a.link", "href", "example.com")` |
| `validation.assert_checked(selector, selector_type=None, timeout=None)` | Assert checkbox is checked | `assert runner.validation.assert_checked("#terms")` |
| `validation.assert_not_checked(selector, selector_type=None, timeout=None)` | Assert checkbox is not checked | `assert runner.validation.assert_not_checked("#newsletter")` |
| `validation.assert_url(expected_url)` | Assert URL equals | `assert runner.validation.assert_url("https://example.com/dashboard")` |
| `validation.assert_url_contains(partial_url)` | Assert URL contains | `assert runner.validation.assert_url_contains("/dashboard")` |
| `validation.assert_title(expected_title)` | Assert title equals | `assert runner.validation.assert_title("Dashboard - Example")` |
| `validation.assert_title_contains(partial_title)` | Assert title contains | `assert runner.validation.assert_title_contains("Dashboard")` |
| `validation.assert_element_count(selector, expected_count, selector_type=None)` | Assert element count equals | `assert runner.validation.assert_element_count(".item", 5)` |
| `validation.assert_element_count_greater_than(selector, min_count, selector_type=None)` | Assert element count is greater than | `assert runner.validation.assert_element_count_greater_than(".result", 3)` |
