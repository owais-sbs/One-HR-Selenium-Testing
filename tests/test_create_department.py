import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "zafar@onehr.com"
PASSWORD = "123456"
LOGIN_ROLE = "company_admin"
DEPARTMENT_NAME = f"Automation Dept {int(time.time())}"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=40)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/company/departments")
    print("Departments page opened")

    add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add Department')]"))
    )
    driver.execute_script("arguments[0].click();", add_button)
    print("Add Department dialog opened")

    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys(DEPARTMENT_NAME)
    print("Department name entered:", DEPARTMENT_NAME)

    try:
        manager_dropdown = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox']"))
        )
        manager_dropdown.click()
        print("Manager dropdown opened")

        first_manager = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
        )
        first_manager.click()
        print("Manager selected")
    except TimeoutException:
        print("No manager selection required")

    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create Department')]"))
    )
    driver.execute_script("arguments[0].click();", create_button)
    print("Create Department clicked")

    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{DEPARTMENT_NAME}')]"))
    )
    print("Department created successfully")

    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver, SCREENSHOT_DIR)

finally:
    driver.quit()
    print("Browser closed")
