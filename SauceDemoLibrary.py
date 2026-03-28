from e2e_class_Structure_flow import (BrowserConfig,LoginPage,InventoryPage,CartPage,CheckoutPage)

class SauceDemoLibrary:
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    """
    Robot Framework custom library for Sauce Demo
    Wraps existing POM page classes as RF Keywords.
    """
    def __init__(self):
        self.driver=None
        self.login_page=None
        self.inventory_page=None
        self.cart_page=None
        self.checkout_page=None

    #-Browser------
    def start_browser(self):
        """Keyword: Start Browser"""
        print("DEBUG: open_browser called")
        self.driver = BrowserConfig.get_driver()
        print("DEBUG: driver created")
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        print("DEBUG: all pages ready")

    def stop_browser(self):
        """Keyword: Stop Browser"""
        if self.driver:
            self.driver.quit()


    #-Login--------
    def open_saucedemo(self):
        """Keyword: Open Saucedemo"""
        self.login_page.open()

    def login(self,username, password):
        """Keyword: Login"""
        self.login_page.login(username, password)


    #--Inventory------------
    def wait_for_load(self):
        """Keyword: Wait For Load"""
        self.inventory_page.wait_for_load()

    def add_to_cart(self):
        """Keyword: Add To Cart"""
        self.inventory_page.add_to_cart()

    def get_cart_count(self):
        """Keyword: Get Cart Count"""
        return self.inventory_page.get_cart_count()

    #-cart----------
    def go_to_cart(self):
        """Keyword: Go To Cart"""
        self.cart_page.cart_page()

    def get_items_name(self):
        """Keyword: Get Items Name"""
        self.cart_page.get_items_name()

    def validation_item_count(self,expected_count):
        """Keyword: Validation Item Count"""
        self.cart_page.validation_item_count(expected_count)

    def proceed_to_checkout(self):
        """Keyword: Proceed To Checkout"""
        self.cart_page.proceed_to_checkout()

    #-Checkout-------
    def fill_customer_info(self,first_name, last_name, postal_code):
        """Keyword: Fill Customer Info"""
        self.checkout_page.fill_customer_info(first_name, last_name, postal_code)

    def complete_order(self):
        """Keyword: Complete Order"""
        self.checkout_page.complete_order()




