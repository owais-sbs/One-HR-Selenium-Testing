import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "kiran.finance@opbs.com"
PASSWORD = "12345678"
LOGIN_ROLE = "finance_manager"
STRUCTURE_NAME = "Automation Salary Structure"
ALLOWANCE_NAME = "HRA"
DEDUCTION_NAME = "Income Tax"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=30)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/payroll/structures/new")
    print("Create Structure page opened")

    structure_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='e.g. Standard Package']"))
    )
    structure_input.clear()
    structure_input.send_keys(STRUCTURE_NAME)
    print("Structure name entered")

    base_salary_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Base Salary')]/following::input[1]"))
    )
    base_salary_input.clear()
    base_salary_input.send_keys("60000")
    print("Base salary entered")

    allowance_add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')][1]"))
    )
    driver.execute_script("arguments[0].click();", allowance_add_button)
    print("Allowance added")

    allowance_name_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Name')])[1]"))
    )
    allowance_name_input.send_keys(ALLOWANCE_NAME)
    print("Allowance name entered")

    allowance_value_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='number'])[2]"))
    )
    allowance_value_input.clear()
    allowance_value_input.send_keys("10")
    print("Allowance value entered")

    deduction_add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')][2]"))
    )
    driver.execute_script("arguments[0].click();", deduction_add_button)
    print("Deduction added")

    deduction_name_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Name')])[2]"))
    )
    deduction_name_input.send_keys(DEDUCTION_NAME)
    print("Deduction name entered")

    deduction_value_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//input[@type='number'])[3]"))
    )
    deduction_value_input.clear()
    deduction_value_input.send_keys("5")
    print("Deduction value entered")

    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create Structure')]"))
    )
    driver.execute_script("arguments[0].click();", create_button)
    print("Create Structure clicked")

    wait.until(EC.url_contains("/payroll/structures"))
    print("Salary structure created successfully")
    time.sleep(5)

except Exception as e:
    print("Test failed:", e)
    screenshot_path = SCREENSHOT_DIR + f"/error_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved:", screenshot_path)

finally:
    driver.quit()
    print("Browser closed")
