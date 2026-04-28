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

START_TIME = "09:30"
END_TIME = "18:30"
BREAK_MINUTES = "60"
GRACE_MINUTES = "15"

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
    # OPEN WORKING HOURS PAGE
    # =============================

    driver.get(
        "http://localhost:3000/settings/working-hours"
    )

    print("Working Hours page opened")

    # =============================
    # WAIT PAGE LOAD
    # =============================

    time.sleep(2)

    # =============================
    # SELECT WORKING DAYS
    # =============================

    print("Selecting working days")

    monday_checkbox = wait.until(
        EC.presence_of_element_located(
            (By.ID, "Monday")
        )
    )

    tuesday_checkbox = driver.find_element(
        By.ID,
        "Tuesday"
    )

    if not monday_checkbox.is_selected():

        driver.execute_script(
            "arguments[0].click();",
            monday_checkbox
        )

    if not tuesday_checkbox.is_selected():

        driver.execute_script(
            "arguments[0].click();",
            tuesday_checkbox
        )

    print("Working days selected")

    # =============================
    # SET START TIME
    # =============================

    start_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@type='time'][1]"
            )
        )
    )

    start_input.clear()
    start_input.send_keys(START_TIME)

    print("Start time set")

    # =============================
    # SET END TIME
    # =============================

    end_input = driver.find_element(
        By.XPATH,
        "(//input[@type='time'])[2]"
    )

    end_input.clear()
    end_input.send_keys(END_TIME)

    print("End time set")

    # =============================
    # SET BREAK MINUTES
    # =============================

    break_input = driver.find_element(
        By.XPATH,
        "(//input[@type='number'])[1]"
    )

    break_input.clear()
    break_input.send_keys(BREAK_MINUTES)

    print("Break minutes set")

    # =============================
    # SET GRACE MINUTES
    # =============================

    grace_input = driver.find_element(
        By.XPATH,
        "(//input[@type='number'])[2]"
    )

    grace_input.clear()
    grace_input.send_keys(GRACE_MINUTES)

    print("Grace minutes set")

    # =============================
    # CLICK SAVE
    # =============================

    save_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Save Changes')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        save_button
    )

    print("Save Changes clicked")

    # =============================
    # VERIFY SUCCESS
    # =============================

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(), 'Working hours saved')]"
            )
        )
    )

    print("Working hours saved successfully")

    time.sleep(5)

except Exception as e:

    print("\n========== ERROR DETAILS ==========\n")

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
        SCREENSHOT_DIR +
        f"/page_{int(time.time())}.html"
    )

    with open(html_path, "w", encoding="utf-8") as f:

        f.write(driver.page_source)

    print("HTML saved:", html_path)

finally:

    driver.quit()

    print("Browser closed")