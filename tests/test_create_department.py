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

USERNAME = "zafar@onehr.com"
PASSWORD = "123456"

DEPARTMENT_NAME = f"Automation Dept {int(time.time())}"

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
    # ROLE SELECTION (OPTIONAL)
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
    # OPEN DEPARTMENTS PAGE
    # =============================

    driver.get(
        "http://localhost:3000/company/departments"
    )

    print("Departments page opened")

    # =============================
    # CLICK ADD DEPARTMENT
    # =============================

    add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Add Department')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        add_button
    )

    print("Add Department dialog opened")

    # =============================
    # ENTER DEPARTMENT NAME
    # =============================

    name_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.ID,
                "name"
            )
        )
    )

    name_input.send_keys(DEPARTMENT_NAME)

    print("Department name entered:", DEPARTMENT_NAME)

    # =============================
    # OPTIONAL — SELECT MANAGER
    # =============================

    try:

        manager_dropdown = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@role='combobox']"
                )
            )
        )

        manager_dropdown.click()

        print("Manager dropdown opened")

        first_manager = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@role='option'][1]"
                )
            )
        )

        first_manager.click()

        print("Manager selected")

    except TimeoutException:

        print("No manager selection required")

    # =============================
    # CLICK CREATE DEPARTMENT
    # =============================

    create_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create Department')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        create_button
    )

    print("Create Department clicked")

    # =============================
    # VERIFY SUCCESS
    # =============================

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//*[contains(text(), '{DEPARTMENT_NAME}')]"
            )
        )
    )

    print("Department created successfully")

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

    print("Screenshot saved:", screenshot_path)

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