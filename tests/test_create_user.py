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

USER_NAME = "Automation User"
USER_EMAIL = f"user{int(time.time())}@test.com"
USER_PASSWORD = "12345678"

ROLE_NAME = "Finance Manager"

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
    # OPEN ADD USER PAGE
    # =============================

    driver.get(
        "http://localhost:3000/settings/users/new"
    )

    print("Add User page opened")

    # =============================
    # ENTER NAME
    # =============================

    name_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='John Doe']"
            )
        )
    )

    name_input.send_keys(USER_NAME)

    print("Name entered")

    # =============================
    # ENTER EMAIL
    # =============================

    email_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@type='email']"
            )
        )
    )

    email_input.send_keys(USER_EMAIL)

    print("Email entered:", USER_EMAIL)

    # =============================
    # ENTER PASSWORD
    # =============================

    password_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='••••••••']"
            )
        )
    )

    password_input.send_keys(USER_PASSWORD)

    print("Password entered")

    # =============================
    # CONFIRM PASSWORD
    # =============================

    confirm_password = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "(//input[@type='password'])[2]"
            )
        )
    )

    confirm_password.send_keys(USER_PASSWORD)

    print("Confirm password entered")

    # =============================
    # SELECT ROLE
    # =============================

    role_card = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//span[contains(text(), '{ROLE_NAME}')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        role_card
    )

    print("Role selected:", ROLE_NAME)

    # =============================
    # CLICK CREATE USER
    # =============================

    create_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create User')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        create_button
    )

    print("Create User clicked")

    # =============================
    # VERIFY SUCCESS
    # =============================

    wait.until(
        EC.url_contains("/settings/users")
    )

    print("User created successfully")

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
        SCREENSHOT_DIR +
        f"/page_{int(time.time())}.html"
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print("HTML saved:", html_path)

finally:

    driver.quit()

    print("Browser closed")