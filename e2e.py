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

options=webdriver.ChromeOptions()
prefs={
    "profile.default_content_setting_values.notifications":2,
    "credentials_enable_service":False,
    "profile.password_manager_enabled":False,
    "profile.password_manager_leak_detection":False,
    "download.default_directory":r"C:\Users\ARUMUGAM\Downloads",
    "download.prompt_for_download":False,
    "download.directory_upgrade":True,
    "safebrowsing.enabled":True,
    "safebrowsing.disable_download_protection":False
}
options.add_experimental_option("prefs",prefs)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("useAutomationExtension",False)
options.add_argument(r"--user-data-dir=C:\ChromeAutomationProfile")
options.add_argument("--maximize-window")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
#options.add_argument("--headless=new")
options.set_capability("acceptInsecureCerts",False)

driver=webdriver.Chrome(options=options)
wait=WebDriverWait(driver,10)
#login_page
driver.get("https://www.saucedemo.com/")
wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@data-test='username']"))).send_keys('standard_user')
driver.find_element(By.XPATH,"//input[@type='password']").send_keys('secret_sauce')
driver.find_element(By.XPATH,"//input[@type='submit']").click()

#cart page
wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'inventory_container')))
cart_button=driver.find_elements(By.XPATH,"//button[contains(text(),'Add to cart')]")
for button in cart_button:
    button.click()

#validating
total_item_in_cart=[item.text for item in driver.find_elements(By.CLASS_NAME,"inventory_item_name ")]
# print(len(total_item_in_cart))
cart_validation=int(driver.find_element(By.CLASS_NAME,'shopping_cart_badge').text)
# print(cart_validation)
assert len(total_item_in_cart)==cart_validation, f"expected count{len(total_item_in_cart)}, matches cart count{cart_validation}"
#storing cart information in json format
# print(total_item_in_cart)
cart_item_price=[item.text for item in driver.find_elements(By.CLASS_NAME,"inventory_item_price")]
#converting to dict format
# cart_details=dict(zip(total_item_in_cart, cart_item_price))
#but we need to in proper format(stripping $ and converting to float)
cart_details={name:float(price.replace("$",""))for name,price in zip(total_item_in_cart, cart_item_price)}
#sorting the value
low_to_high=dict(sorted(cart_details.items(),key=lambda x:x[1]))
high_to_low=dict(sorted(cart_details.items(),key=lambda x:x[1],reverse=True))
# print(cart_details)
# print(low_to_high)
# print(high_to_low)
#updating_data
# test_data={
#     "page":"Cart_page",
#     "products":cart_details,
#     "total_products":len(cart_details)
# }
# with open("file.json",'w') as f:
#     json.dump(test_data,f,indent=4)
#check_out Page:
wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'shopping_cart_badge'))).click()
check_out_items=[item.text for item in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'inventory_item_name')))]
assert cart_validation==len(check_out_items),f"purchased count{cart_validation},does not matches {len(check_out_items)}"
driver.find_element(By.XPATH,"//button[contains(text(),'Checkout')]").click()
#customer_information
wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'checkout_info')))
driver.find_element(By.ID,'first-name').send_keys('Aru')
driver.find_element(By.ID,'last-name').send_keys('Bhai')
driver.find_element(By.ID,'postal-code').send_keys('789654')
driver.find_element(By.ID,'continue').click()
#summary_page
wait.until(EC.presence_of_all_elements_located((By.ID,'checkout_summary_container')))
driver.find_element(By.ID,'finish').click()
time.sleep(5)
driver.quit()
