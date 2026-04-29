import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "zafar@onehr.com"
PASSWORD = "123456"
LOGIN_ROLE = "company_admin"
USER_NAME = "Automation User"
USER_EMAIL = f"user{int(time.time())}@test.com"
USER_PASSWORD = "12345678"
ROLE_NAME = "Finance Manager"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=40)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/settings/users/new")
    print("Add User page opened")

    name_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='John Doe']"))
    )
    name_input.send_keys(USER_NAME)
    print("Name entered")

    email_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    email_input.send_keys(USER_EMAIL)
    print("Email entered:", USER_EMAIL)

    password_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='••••••••']"))
    )
    password_input.send_keys(USER_PASSWORD)
    print("Password entered")

    confirm_password = wait.until(
        EC.visibility_of_element_located((By.XPATH, "(//input[@type='password'])[2]"))
    )
    confirm_password.send_keys(USER_PASSWORD)
    print("Confirm password entered")

    role_card = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{ROLE_NAME}')]"))
    )
    driver.execute_script("arguments[0].click();", role_card)
    print("Role selected:", ROLE_NAME)

    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create User')]"))
    )
    driver.execute_script("arguments[0].click();", create_button)
    print("Create User clicked")

    wait.until(EC.url_contains("/settings/users"))
    print("User created successfully")
    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver, SCREENSHOT_DIR)

finally:
    driver.quit()
    print("Browser closed")
