import pytest
from e2e_project.e2e_class_Structure_flow import BrowserConfig,LoginPage,InventoryPage,CartPage,CheckoutPage
@pytest.fixture
def driver():
    driver=BrowserConfig.get_driver()
    yield driver
    driver.quit()

# logged_in_driver depends on driver fixture
@pytest.fixture
def login(driver): # ← takes driver fixture as argument
    login_page=LoginPage(driver)
    login_page.open()
    login_page.login("standard_user","secret_sauce")
    assert "inventory" in driver.current_url
    print("[PASS] Login successful")
    yield driver