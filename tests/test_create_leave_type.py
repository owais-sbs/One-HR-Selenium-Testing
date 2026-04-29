import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "abdulhameed@opbs.com"
PASSWORD = "123456"
LOGIN_ROLE = "hr_manager"
LEAVE_NAME = f"Automation Leave {int(time.time())}"
TOTAL_DAYS = "12"
MAX_CARRY = "5"

SCREENSHOT_DIR = "screenshots"
HTML_DIR = "error_html"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

driver, wait = create_driver(timeout=40)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/settings/leave")
    print("Leave settings page opened")

    add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add Leave Type')]"))
    )
    driver.execute_script("arguments[0].click();", add_button)
    print("Add Leave Type dialog opened")

    name_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='e.g. Annual Leave']"))
    )
    name_input.send_keys(LEAVE_NAME)
    print("Leave name entered")

    total_days_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='number']"))
    )
    total_days_input.clear()
    total_days_input.send_keys(TOTAL_DAYS)
    print("Total days entered")

    try:
        carry_switch = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']"))
        )
        driver.execute_script("arguments[0].click();", carry_switch)
        print("Carry forward enabled")

        max_carry_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='number'])[2]"))
        )
        max_carry_input.clear()
        max_carry_input.send_keys(MAX_CARRY)
        print("Max carry entered")
    except TimeoutException:
        print("Carry forward optional — skipped")

    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create')]"))
    )
    driver.execute_script("arguments[0].click();", create_button)
    print("Create Leave Type clicked")

    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{LEAVE_NAME}')]"))
    )
    print("Leave type created successfully")
    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver, SCREENSHOT_DIR, HTML_DIR)

finally:
    driver.quit()
    print("Browser closed")
