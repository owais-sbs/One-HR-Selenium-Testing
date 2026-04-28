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

COUNTRY_NAME = "Test Country"
CURRENCY = "USD"

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

wait = WebDriverWait(driver, 25)

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
    # OPEN COUNTRIES PAGE
    # =============================

    driver.get(
        "http://localhost:3000/master-data/countries"
    )

    print("Navigated to Countries page")

    # =============================
    # CLICK ADD COUNTRY LINK
    # =============================

    add_country_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(@href,'/master-data/countries/new')]"
            )
        )
    )

    add_country_link.click()

    print("Add Country page opened")

    # =============================
    # VERIFY NEW PAGE
    # =============================

    wait.until(
        EC.url_contains("/countries/new")
    )

    print("New Country form loaded")

    # =============================
    # ENTER COUNTRY NAME
    # =============================

    name_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[contains(@placeholder,'Country')]"
            )
        )
    )

    name_input.send_keys(COUNTRY_NAME)

    print("Country name entered")

    # =============================
    # ENTER CURRENCY
    # =============================

    currency_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[contains(@placeholder,'Currency')]"
            )
        )
    )

    currency_input.send_keys(CURRENCY)

    print("Currency entered")

    # =============================
    # CLICK SAVE
    # =============================

    save_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Save')]"
            )
        )
    )

    save_button.click()

    print("Save clicked")

    # =============================
    # VERIFY SUCCESS
    # =============================

    try:

        wait.until(
            EC.url_contains("/countries")
        )

        print("Country created successfully")

    except TimeoutException:

        print("Success verification failed")

    time.sleep(5)

except Exception as e:

    print("Test failed:", e)

    timestamp = int(time.time())

    screenshot_path = f"{SCREENSHOT_DIR}/error_{timestamp}.png"

    driver.save_screenshot(screenshot_path)

    print("Screenshot saved:", screenshot_path)

finally:

    driver.quit()

    print("Browser closed")