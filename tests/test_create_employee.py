from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

import time
import os
import traceback

# =============================
# CONFIG
# =============================

BASE_URL = "http://localhost:3000"

USERNAME = "mustafa.hr@opbs.com"
PASSWORD = "12345678"

FIRST_NAME = "Test"
LAST_NAME = "Employee"

EMAIL = f"emp{int(time.time())}@test.com"
EMP_PASSWORD = "123456"

PHONE = "9876543210"

DEPARTMENT_ID = "1"
DESIGNATION_ID = "1"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =============================
# START BROWSER
# =============================

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

driver.maximize_window()

wait = WebDriverWait(driver, 40)

# =============================
# HELPER — Continue button
# =============================

def click_continue_and_wait(next_field_id):

    print("Waiting for Continue button...")

    continue_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Continue')]"
            )
        )
    )

    print("Continue button found")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        continue_button
    )

    time.sleep(1)

    driver.execute_script(
        "arguments[0].click();",
        continue_button
    )

    print("Continue clicked")

    print("Waiting for next step:", next_field_id)

    wait.until(
        EC.visibility_of_element_located(
            (
                By.ID,
                next_field_id
            )
        )
    )

    print("Next step loaded")


try:

    print("Opening login page")

    driver.get(BASE_URL)

    # =============================
    # LOGIN
    # =============================

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "username")
        )
    ).send_keys(USERNAME)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "password")
        )
    ).send_keys(PASSWORD)

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    ).click()

    print("Login submitted")

    # =============================
    # ROLE SELECTION
    # =============================

    try:

        role_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Super Admin')]"
                )
            )
        )

        role_button.click()

        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'Continue')]"
                )
            )
        ).click()

        print("Role selected")

    except TimeoutException:

        print("Role selection not required")

    wait.until(
        EC.url_contains("/dashboard")
    )

    print("Dashboard opened")

    # =============================
    # OPEN CREATE EMPLOYEE PAGE
    # =============================

    driver.get(
        "http://localhost:3000/employees/new"
    )

    print("Create Employee page opened")

    # =============================
    # STEP 1
    # =============================

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "firstName")
        )
    ).send_keys(FIRST_NAME)

    driver.find_element(
        By.ID,
        "lastName"
    ).send_keys(LAST_NAME)

    driver.find_element(
        By.ID,
        "email"
    ).send_keys(EMAIL)

    driver.find_element(
        By.ID,
        "password"
    ).send_keys(EMP_PASSWORD)

    driver.find_element(
        By.ID,
        "phone"
    ).send_keys(PHONE)

    print("Step 1 completed")

    click_continue_and_wait("emergencyContactName")

    # =============================
    # STEP 2
    # =============================

    driver.find_element(
        By.ID,
        "emergencyContactName"
    ).send_keys("Father")

    driver.find_element(
        By.ID,
        "emergencyContactRelationship"
    ).send_keys("Parent")

    driver.find_element(
        By.ID,
        "emergencyContactPhone"
    ).send_keys("9999999999")

    print("Step 2 completed")

    click_continue_and_wait("department")

    # =============================
    # STEP 3
    # =============================

    department_dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "department")
        )
    )

    department_dropdown.send_keys(DEPARTMENT_ID)

    driver.find_element(
        By.ID,
        "designation"
    ).send_keys(DESIGNATION_ID)

    driver.find_element(
        By.ID,
        "joiningDate"
    ).send_keys("2026-01-01")

    print("Step 3 completed")

    click_continue_and_wait("salaryStructure")

    # =============================
    # STEP 4
    # =============================

    salary_dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "salaryStructure")
        )
    )

    salary_dropdown.click()

    time.sleep(1)

    salary_dropdown.send_keys("1")

    print("Step 4 completed")

    click_continue_and_wait("Submit")

    # =============================
    # STEP 5 — SUBMIT
    # =============================

    submit_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Submit')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        submit_button
    )

    print("Employee submitted")

    wait.until(
        EC.url_contains("/employees")
    )

    print("Employee created successfully")

    time.sleep(5)

except Exception as e:

    print("\n================ ERROR DETAILS ================\n")

    print("Error message:")
    print(str(e))

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nPage title:")
    print(driver.title)

    print("\nStacktrace:")
    traceback.print_exc()

    screenshot_path = (
        SCREENSHOT_DIR +
        f"/error_{int(time.time())}.png"
    )

    driver.save_screenshot(screenshot_path)

    print("\nScreenshot saved:", screenshot_path)

    html_path = (
        SCREENSHOT_DIR +
        f"/page_{int(time.time())}.html"
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("HTML saved:", html_path)

finally:

    driver.quit()

    print("Browser closed")