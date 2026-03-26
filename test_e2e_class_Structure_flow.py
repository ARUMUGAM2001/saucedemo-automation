import pytest
from e2e_project.e2e_class_Structure_flow import BrowserConfig,LoginPage,InventoryPage,CartPage,CheckoutPage



# @pytest.fixture
# def driver():
#     driver=BrowserConfig.get_driver()
#     yield driver
#     driver.quit()
#
# # logged_in_driver depends on driver fixture
# @pytest.fixture
# def login(driver): # ← takes driver fixture as argument
#     login_page=LoginPage(driver)
#     login_page.open()
#     login_page.login("standard_user","secret_sauce")
#     assert "inventory" in driver.current_url
#     print("[PASS] Login successful")
#     yield driver


def test_add_to_cart(login):
    inventory_page = InventoryPage(login)
    inventory_page.wait_for_load()
    inventory_page.add_to_cart()

    cart=CartPage(login)
    cart.cart_page()
    cart.validation_item_count(inventory_page.get_cart_count())
    cart.proceed_to_checkout()

def test_checkout(login):
    inventory_page = InventoryPage(login)
    inventory_page.wait_for_load()
    inventory_page.add_to_cart()

    cart = CartPage(login)
    cart.cart_page()
    cart.validation_item_count(inventory_page.get_cart_count())
    cart.proceed_to_checkout()

    checkout_page = CheckoutPage(login)
    checkout_page.fill_customer_info("Aru","Don","234567")
    checkout_page.complete_order()




