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

USERNAME = "kiran@admin.com"
PASSWORD = "123456"

SUPER_ADMIN_NAME = "Test Super Admin"

timestamp = int(time.time())

SUPER_ADMIN_EMAIL = f"superadmin{timestamp}@test.com"

SUPER_ADMIN_PASSWORD = "123456"

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

    wait.until(
        EC.url_contains("/dashboard")
    )

    print("Dashboard opened")

    # =============================
    # OPEN SUPER ADMINS PAGE
    # =============================

    driver.get(
        "http://localhost:3000/super-admins"
    )

    print("Super Admin page opened")

    # =============================
    # CLICK ADD BUTTON
    # =============================

    add_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Add Super Admin')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        add_button
    )

    time.sleep(1)

    driver.execute_script(
        "arguments[0].click();",
        add_button
    )

    print("Add Super Admin clicked")

    # =============================
    # FILL FORM
    # =============================

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "sa-name")
        )
    ).send_keys(SUPER_ADMIN_NAME)

    print("Name entered")

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "sa-email")
        )
    ).send_keys(SUPER_ADMIN_EMAIL)

    print("Dynamic email used:", SUPER_ADMIN_EMAIL)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "sa-password")
        )
    ).send_keys(SUPER_ADMIN_PASSWORD)

    print("Password entered")

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "sa-confirm")
        )
    ).send_keys(SUPER_ADMIN_PASSWORD)

    print("Confirm password entered")

    # =============================
    # CLICK CREATE
    # =============================

    create_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[contains(., 'Create Super Admin')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        create_button
    )

    time.sleep(1)

    driver.execute_script(
        "arguments[0].click();",
        create_button
    )

    print("Create Super Admin clicked")

    # =============================
    # VERIFY
    # =============================

    try:

        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{SUPER_ADMIN_EMAIL}')]"
                )
            )
        )

        print("Super Admin created successfully")

    except TimeoutException:

        print("Super Admin creation verification failed")

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