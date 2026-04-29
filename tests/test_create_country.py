import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import create_driver, login, dismiss_any_popup, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "kiran@admin.com"
PASSWORD = "123456"
LOGIN_ROLE = "super_admin"
COUNTRY_NAME = "Test Country"
CURRENCY = "USD"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=25)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/master-data/countries")
    print("Navigated to Countries page")

    add_country_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/master-data/countries/new')]"))
    )
    add_country_link.click()
    print("Add Country page opened")

    wait.until(EC.url_contains("/countries/new"))
    print("New Country form loaded")

    name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Country')]"))
    )
    name_input.send_keys(COUNTRY_NAME)
    print("Country name entered")

    currency_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Currency')]"))
    )
    currency_input.send_keys(CURRENCY)
    print("Currency entered")

    save_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
    )
    save_button.click()
    print("Save clicked")

    try:
        wait.until(EC.url_contains("/countries"))
        print("Country created successfully")
    except TimeoutException:
        print("Success verification failed")

    time.sleep(5)

except Exception as e:
    print("Test failed:", e)
    screenshot_path = f"{SCREENSHOT_DIR}/error_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved:", screenshot_path)

finally:
    driver.quit()
    print("Browser closed")
