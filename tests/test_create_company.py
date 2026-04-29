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
COMPANY_NAME = "Test Automation Company"
COMPANY_CODE = "TAC"
COUNTRY_NAME = "India"

timestamp = int(time.time())
ADMIN_EMAIL = f"admin{timestamp}@test.com"
ADMIN_PASSWORD = "123456"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=30)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/superadmin/companies/new")
    print("Add Company page opened")

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter company name']"))
    ).send_keys(COMPANY_NAME)
    print("Company name entered")

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='e.g. ACM']"))
    ).send_keys(COMPANY_CODE)
    print("Company code entered")

    country_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search country...']"))
    )
    country_input.send_keys(COUNTRY_NAME)
    print("Country search entered")

    country_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{COUNTRY_NAME}')]"))
    )
    country_option.click()
    print("Country selected")

    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(1)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='admin@company.com']"))
    ).send_keys(ADMIN_EMAIL)
    print("Dynamic email used:", ADMIN_EMAIL)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Create admin password']"))
    ).send_keys(ADMIN_PASSWORD)
    print("Password entered")

    create_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Create Company')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", create_button)
    print("Create Company clicked")

    try:
        wait.until(EC.url_contains("/companies"))
        print("Company created successfully")
    except TimeoutException:
        print("Company creation verification failed")

    time.sleep(5)

except Exception as e:
    print("Test failed:", e)
    screenshot_path = SCREENSHOT_DIR + f"/error_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved:", screenshot_path)

finally:
    driver.quit()
    print("Browser closed")
