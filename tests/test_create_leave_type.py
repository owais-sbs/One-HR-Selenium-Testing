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

USERNAME = "abdulhameed@opbs.com"
PASSWORD = "123456"

LEAVE_NAME = f"Automation Leave {int(time.time())}"
TOTAL_DAYS = "12"
MAX_CARRY = "5"

SCREENSHOT_DIR = "screenshots"

HTML_DIR = "error_html"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

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
    # OPEN LEAVE SETTINGS PAGE
    # =============================

    driver.get(
        "http://localhost:3000/settings/leave"
    )

    print("Leave settings page opened")

    # =============================
    # CLICK ADD LEAVE TYPE
    # =============================

    add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Add Leave Type')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        add_button
    )

    print("Add Leave Type dialog opened")

    # =============================
    # ENTER NAME
    # =============================

    name_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. Annual Leave']"
            )
        )
    )

    name_input.send_keys(LEAVE_NAME)

    print("Leave name entered")

    # =============================
    # ENTER TOTAL DAYS
    # =============================

    total_days_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@type='number']"
            )
        )
    )

    total_days_input.clear()
    total_days_input.send_keys(TOTAL_DAYS)

    print("Total days entered")

    # =============================
    # ENABLE CARRY FORWARD
    # =============================

    try:

        carry_switch = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@role='switch']"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            carry_switch
        )

        print("Carry forward enabled")

        max_carry_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "(//input[@type='number'])[2]"
                )
            )
        )

        max_carry_input.clear()
        max_carry_input.send_keys(MAX_CARRY)

        print("Max carry entered")

    except TimeoutException:

        print("Carry forward optional — skipped")

    # =============================
    # CLICK CREATE
    # =============================

    create_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        create_button
    )

    print("Create Leave Type clicked")

    # =============================
    # VERIFY SUCCESS
    # =============================

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//*[contains(text(), '{LEAVE_NAME}')]"
            )
        )
    )

    print("Leave type created successfully")

    time.sleep(5)

except Exception as e:

    print("\n================ ERROR DETAILS ================\n")

    print("Error message:")
    print(str(e))

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nStacktrace:")
    traceback.print_exc()

    screenshot_path = (
        SCREENSHOT_DIR +
        f"/error_{int(time.time())}.png"
    )

    driver.save_screenshot(screenshot_path)

    print("Screenshot saved:", screenshot_path)

    html_path = (
        HTML_DIR +
        f"/error_page_{int(time.time())}.html"
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("HTML saved:", html_path)

finally:

    driver.quit()

    print("Browser closed")