from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

import time
import os

# =============================
# CONFIG
# =============================

BASE_URL = "http://localhost:3000"

USERNAME = "kiran.finance@opbs.com"
PASSWORD = "12345678"

STRUCTURE_NAME = "Automation Salary Structure"

ALLOWANCE_NAME = "HRA"
DEDUCTION_NAME = "Income Tax"

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

wait = WebDriverWait(driver, 30)

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
    # OPTIONAL ROLE SELECTION
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

    # =============================
    # VERIFY LOGIN
    # =============================

    wait.until(
        EC.url_contains("/dashboard")
    )

    print("Dashboard opened")

    # =============================
    # OPEN CREATE STRUCTURE PAGE
    # =============================

    driver.get(
        "http://localhost:3000/payroll/structures/new"
    )

    print("Create Structure page opened")

    # =============================
    # STRUCTURE NAME
    # =============================

    structure_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@placeholder='e.g. Standard Package']"
            )
        )
    )

    structure_input.clear()
    structure_input.send_keys(STRUCTURE_NAME)

    print("Structure name entered")

    # =============================
    # BASE SALARY (FIXED LOCATOR)
    # =============================

    base_salary_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//label[contains(., 'Base Salary')]/following::input[1]"
            )
        )
    )

    base_salary_input.clear()
    base_salary_input.send_keys("60000")

    print("Base salary entered")

    # =============================
    # ADD ALLOWANCE
    # =============================

    allowance_add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Add')][1]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        allowance_add_button
    )

    print("Allowance added")

    # Allowance Name

    allowance_name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "(//input[contains(@placeholder,'Name')])[1]"
            )
        )
    )

    allowance_name_input.send_keys(ALLOWANCE_NAME)

    print("Allowance name entered")

    # Allowance Value

    allowance_value_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "(//input[@type='number'])[2]"
            )
        )
    )

    allowance_value_input.clear()
    allowance_value_input.send_keys("10")

    print("Allowance value entered")

    # =============================
    # ADD DEDUCTION
    # =============================

    deduction_add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Add')][2]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        deduction_add_button
    )

    print("Deduction added")

    deduction_name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "(//input[contains(@placeholder,'Name')])[2]"
            )
        )
    )

    deduction_name_input.send_keys(DEDUCTION_NAME)

    print("Deduction name entered")

    deduction_value_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "(//input[@type='number'])[3]"
            )
        )
    )

    deduction_value_input.clear()
    deduction_value_input.send_keys("5")

    print("Deduction value entered")

    # =============================
    # CLICK CREATE
    # =============================

    create_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create Structure')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        create_button
    )

    print("Create Structure clicked")

    # =============================
    # VERIFY
    # =============================

    wait.until(
        EC.url_contains(
            "/payroll/structures"
        )
    )

    print("Salary structure created successfully")

    time.sleep(5)

except Exception as e:

    print("Test failed:", e)

    screenshot_path = (
        SCREENSHOT_DIR +
        f"/error_{int(time.time())}.png"
    )

    driver.save_screenshot(screenshot_path)

    print("Screenshot saved:", screenshot_path)

finally:

    driver.quit()

    print("Browser closed")