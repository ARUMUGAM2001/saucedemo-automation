import traceback
import selenium
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys



class BrowserConfig:
    """Handles Chrome browser configuration and download installation"""

    DOWNLOAD_DIR=r'C:\Users\ARUMUGAM\Downloads'
    USER_DATA_DIR=r'C:\Users\ChromeAutomationProfile'

    @staticmethod
    def get_driver() -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "download.default_directory": r"C:\Users\ARUMUGAM\Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        #options.add_argument(r"--user-data-dir=C:\ChromeAutomationProfile")
        options.add_argument("--maximize-window")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        #options.add_argument("--headless=new")
        options.set_capability("acceptInsecureCerts", False)

        return webdriver.Chrome(options=options)


class SauceDemoPage:
    """Base page holding shared driver and wait instance"""

    BASE_URL="https://www.saucedemo.com"

    def __init__(self,driver: webdriver.Chrome,timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)


class LoginPage(SauceDemoPage):
    """Handle Login page Interactions"""

    #locators
    USERNAME_INPUT=(By.XPATH, "//input[@data-test='username']")
    PASSWORD_INPUT=(By.XPATH, "//input[@type='password']")
    SUBMIT_BUTTON=(By.XPATH, "//input[@type='submit']")

    def open(self):
        self.driver.get(self.BASE_URL)

    def login(self,user_name:str,password:str):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(
            user_name)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()


class InventoryPage(SauceDemoPage):
    """Handle Inventory page Interactions"""

    INVENTORY_LIST=(By.CLASS_NAME, 'inventory_container')
    ADD_TO_CART_BUTTON=(By.XPATH, "//button[contains(text(),'Add to cart')]")
    ITEM_NAME=(By.CLASS_NAME, "inventory_item_name ")
    COUNT_OF_CART_ITEM=(By.CLASS_NAME, 'shopping_cart_badge')
    ITEM_PRICE=(By.CLASS_NAME, "inventory_item_price")

    def wait_for_load(self ):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_LIST))

    def add_to_cart(self):
        cart_button = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
        for button in cart_button:
            button.click()

    def get_item_name(self) ->list[str]:
        total_item_in_cart = [item.text for item in self.driver.find_elements(*self.ITEM_NAME)]
        return total_item_in_cart

    def get_cart_count(self) ->int:
        cart_validation = int(self.driver.find_element(*self.COUNT_OF_CART_ITEM).text)
        return cart_validation

    def get_cart_price(self) ->dict[str,float]:
        name=self.get_item_name()
        price = [item.text for item in self.driver.find_elements(*self.ITEM_PRICE)]
        cart_details = {name: float(price.replace("$", "")) for name, price in zip(name, price)}
        return cart_details

    def validate_card_count(self):
        name=self.get_item_name()
        card_count = self.get_cart_count()
        assert len(name)==card_count,(
            f"Expected card count {len(name)} , but got {card_count} instead"
        )
        print(f"[PASS] Cart badge count matches: {card_count} items")

    def get_sorted_card_details(self,details: dict[str,float])->dict:
        low_to_high = dict(sorted(details.items(), key=lambda x: x[1]))
        high_to_low = dict(sorted(details.items(), key=lambda x: x[1], reverse=True))
        return {"low_to_high":low_to_high,"high_to_low":high_to_low}

    def save_to_json(self,cart_details: dict[str,float],filepath: str="file.json"):
        test_data={
            "page":"Cart_page",
            "products":cart_details,
            "total_products":len(cart_details)
        }
        with open(filepath,'w') as f:
            json.dump(test_data,f,indent=4)
        print(f"[INFO] Cart data saved to {filepath}")


class CartPage(SauceDemoPage):
    """Handles cart page /and checkout interaction"""

    CART_NAV=(By.CLASS_NAME, 'shopping_cart_badge')
    INVENTORY_ITEM=(By.CLASS_NAME, 'inventory_item_name')
    CHECK_OUT_NAV=(By.XPATH, "//button[contains(text(),'Checkout')]")

    def cart_page(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_NAV)).click()

    def get_items_name(self) ->list[str]:
        item_name = [item.text for item in
                           self.wait.until(EC.presence_of_all_elements_located(self.INVENTORY_ITEM))]
        return item_name

    def validation_item_count(self,expected_count: int):
        items=self.get_items_name()

        assert expected_count == len(
            items), f"purchased count{expected_count},does not matches {len(items)}"
        print(f"[PASS] purchased count{expected_count},matches {len(items)}")

    def proceed_to_checkout(self):
        self.driver.find_element(*self.CHECK_OUT_NAV).click()


class CheckoutPage(SauceDemoPage):
    """Handles the checkout information and summary page"""

    CHECK_OUT_INFO=(By.CLASS_NAME, 'checkout_info')
    FIRST_NAME=(By.ID, 'first-name')
    LAST_NAME=(By.ID, 'last-name')
    POSTAL_CODE=(By.ID, 'postal-code')
    PROCEED_TO_SUMMARY=(By.ID, 'continue')
    SUMMARY_PAGE=(By.ID, 'checkout_summary_container')
    COMPLETE_PURCHASE=(By.ID, 'finish')

    def fill_customer_info(self,first_name:str,last_name:str,postal_code:str):
        self.wait.until(EC.visibility_of_element_located(self.CHECK_OUT_INFO))
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)
        self.driver.find_element(*self.PROCEED_TO_SUMMARY).click()

    def complete_order(self):
        self.wait.until(EC.presence_of_all_elements_located(self.SUMMARY_PAGE))
        self.driver.find_element(*self.COMPLETE_PURCHASE).click()
        print(f"[PASS] Order Placed Successfully")


class SauceDemoTest:

    """
        Orchestrates the full end-to-end for saucedemo.com

        Flow:
            1.Login Page.
            2.Product selection and count validation.
            3.Navigate to cart & validate item count.
            4.Checkout with customer information
            5.Complete the order

    """
    CREDENTIALS={"user_name":"standard_user","password":"secret_sauce"}
    CUSTOMER={"first_name":"Aru","last_name":"Bhai","postal_code":"675839"}

    def __init__(self):
        self.driver = BrowserConfig.get_driver()

    def run(self):
        try:
            #---- step 1: login ------
            login_page=LoginPage(self.driver)
            login_page.open()
            login_page.login(**self.CREDENTIALS)
            print("[INFO] Logged in successfully.")

            #----step 2: Inventory / Add to Cart
            inventory_page=InventoryPage(self.driver)
            inventory_page.wait_for_load()
            inventory_page.add_to_cart()
            inventory_page.validate_card_count()
            card_details=inventory_page.get_cart_price()
            sorted_data=inventory_page.get_sorted_card_details(card_details)
            print(f"[INFO] Low → High: {sorted_data['low_to_high']}")
            print(f"[INFO] High → Low: {sorted_data['high_to_low']}")
            #---save the data if required---

            #---step3 cart_page---
            cart=CartPage(self.driver)
            cart.cart_page()
            cart.get_items_name()
            cart.validation_item_count(inventory_page.get_cart_count())
            cart.proceed_to_checkout()

            #---step4 & step5 order_submission--
            checkout_page=CheckoutPage(self.driver)
            checkout_page.fill_customer_info(**self.CUSTOMER)
            checkout_page.complete_order()

            time.sleep(5)

        except AssertionError as e:
            print(f"[FAIL] Assertion Failed: {e}")
            traceback.print_exc()

        except Exception as e:
            print(f"[ERROR]unexpected error {e}")
            traceback.print_exc()
        finally:
            self.driver.quit()
            print("[INFO] Browser closed.")

if __name__=="__main__":
    test=SauceDemoTest()
    test.run()