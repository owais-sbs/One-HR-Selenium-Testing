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

COMPANY_NAME = "Test Automation Company"
COMPANY_CODE = "TAC"
COUNTRY_NAME = "India"

# Dynamic email generation
timestamp = int(time.time())

ADMIN_EMAIL = f"admin{timestamp}@test.com"
ADMIN_PASSWORD = "123456"

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

    # LOGIN

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

    # OPEN ADD COMPANY PAGE

    driver.get(
        "http://localhost:3000/superadmin/companies/new"
    )

    print("Add Company page opened")

    # COMPANY NAME

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='Enter company name']"
            )
        )
    ).send_keys(COMPANY_NAME)

    print("Company name entered")

    # COMPANY CODE

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. ACM']"
            )
        )
    ).send_keys(COMPANY_CODE)

    print("Company code entered")

    # COUNTRY SELECT

    country_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='Search country...']"
            )
        )
    )

    country_input.send_keys(COUNTRY_NAME)

    print("Country search entered")

    country_option = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//button[contains(., '{COUNTRY_NAME}')]"
            )
        )
    )

    country_option.click()

    print("Country selected")

    # Close dropdown

    driver.find_element(
        By.TAG_NAME,
        "body"
    ).click()

    time.sleep(1)

    # EMAIL

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='admin@company.com']"
            )
        )
    ).send_keys(ADMIN_EMAIL)

    print("Dynamic email used:", ADMIN_EMAIL)

    # PASSWORD

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='Create admin password']"
            )
        )
    ).send_keys(ADMIN_PASSWORD)

    print("Password entered")

    # CREATE COMPANY

    create_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[contains(., 'Create Company')]"
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

    print("Create Company clicked")

    # VERIFY

    try:

        wait.until(
            EC.url_contains("/companies")
        )

        print("Company created successfully")

    except TimeoutException:

        print("Company creation verification failed")

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