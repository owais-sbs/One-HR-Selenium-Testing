import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "mustafa.hr@opbs.com"
PASSWORD = "12345678"
LOGIN_ROLE = "hr_manager"
FIRST_NAME = "Test"
LAST_NAME = "Employee"
EMAIL = f"emp{int(time.time())}@test.com"
EMP_PASSWORD = "123456"
PHONE = "9876543210"
DEPARTMENT_ID = "1"
DESIGNATION_ID = "1"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=40)


def click_continue_and_wait(driver, wait, next_field_id):
    print("Waiting for Continue button...")
    continue_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
    )
    print("Continue button found")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", continue_button)
    print("Continue clicked")
    print("Waiting for next step:", next_field_id)
    wait.until(EC.visibility_of_element_located((By.ID, next_field_id)))
    print("Next step loaded")


try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/employees/new")
    print("Create Employee page opened")

    wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys(FIRST_NAME)
    driver.find_element(By.ID, "lastName").send_keys(LAST_NAME)
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(EMP_PASSWORD)
    driver.find_element(By.ID, "phone").send_keys(PHONE)
    print("Step 1 completed")
    click_continue_and_wait(driver, wait, "emergencyContactName")

    driver.find_element(By.ID, "emergencyContactName").send_keys("Father")
    driver.find_element(By.ID, "emergencyContactRelationship").send_keys("Parent")
    driver.find_element(By.ID, "emergencyContactPhone").send_keys("9999999999")
    print("Step 2 completed")
    click_continue_and_wait(driver, wait, "department")

    department_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "department")))
    department_dropdown.send_keys(DEPARTMENT_ID)
    driver.find_element(By.ID, "designation").send_keys(DESIGNATION_ID)
    driver.find_element(By.ID, "joiningDate").send_keys("2026-01-01")
    print("Step 3 completed")
    click_continue_and_wait(driver, wait, "salaryStructure")

    salary_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "salaryStructure")))
    salary_dropdown.click()
    time.sleep(1)
    salary_dropdown.send_keys("1")
    print("Step 4 completed")
    click_continue_and_wait(driver, wait, "Submit")

    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]"))
    )
    driver.execute_script("arguments[0].click();", submit_button)
    print("Employee submitted")

    wait.until(EC.url_contains("/employees"))
    print("Employee created successfully")
    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver, SCREENSHOT_DIR)

finally:
    driver.quit()
    print("Browser closed")
