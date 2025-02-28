import time
from tests.common_tests import _login, _form_interactions, _multiple_selector_types, _dynamic_waits, _table_interaction
from config import Config

config = Config()

def test_login(runner):
    loginPage = "https://the-internet.herokuapp.com/login"
    username = config.LOGIN_USERNAME
    password = config.LOGIN_PASSWORD
    _login(runner, loginPage, username, password)

def test_form_interactions(runner):
    formPage = "https://the-internet.herokuapp.com/dropdown"
    checkboxesPage = "https://the-internet.herokuapp.com/checkboxes"
    _form_interactions(runner, formPage, checkboxesPage)

def test_multiple_selector_types(runner):
    loginPage = "https://the-internet.herokuapp.com/login"
    username = config.LOGIN_USERNAME
    password = config.LOGIN_PASSWORD
    _multiple_selector_types(runner, loginPage, username, password)

def test_dynamic_waits(runner):    
    loadingPage = "https://the-internet.herokuapp.com/dynamic_loading/1"
    _dynamic_waits(runner, loadingPage)

def test_table_interaction(runner):
    """
    Test interacting with tables using dynamic selectors
    """
    tablePage = "https://the-internet.herokuapp.com/tables"
    _table_interaction(runner, tablePage)