from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# =============================
# CONFIG
# =============================

BASE_URL = "http://localhost:3000"

USERNAME = "zafar@onehr.com"
PASSWORD = "123456"

# =============================
# START BROWSER
# =============================

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

driver.maximize_window()

wait = WebDriverWait(driver, 20)

try:
    print("Opening login page...")

    driver.get(BASE_URL)

    # =============================
    # ENTER USERNAME
    # =============================

    username_input = wait.until(
        EC.presence_of_element_located(
            (By.ID, "username")
        )
    )

    username_input.clear()
    username_input.send_keys(USERNAME)

    # =============================
    # ENTER PASSWORD
    # =============================

    password_input = wait.until(
        EC.presence_of_element_located(
            (By.ID, "password")
        )
    )

    password_input.clear()
    password_input.send_keys(PASSWORD)

    # =============================
    # CLICK LOGIN
    # =============================

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )

    login_button.click()

    print("Login submitted")

    # =============================
    # HANDLE ROLE SELECTION (OPTIONAL)
    # =============================

    try:
        role_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Super Admin')]")
            )
        )

        role_button.click()

        continue_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Continue')]")
            )
        )

        continue_button.click()

        print("Role selected")

    except TimeoutException:
        print("Role selection not required")

    # =============================
    # CHECK SUCCESS OR ERROR
    # =============================

    try:
        # SUCCESS CASE
        wait.until(
            EC.url_contains("/dashboard")
        )

        print("Login SUCCESS")
        print("Dashboard URL:", driver.current_url)

    except TimeoutException:

        # ERROR CASE
        try:
            error_message = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//p[contains(text(),'No supported roles')]"
                    )
                )
            )

            print("Login FAILED — Role not supported")
            print("Error message:", error_message.text)

        except TimeoutException:
            print("Login status unknown")

    time.sleep(5)

except Exception as e:
    print("Test failed:", e)

finally:
    driver.quit()
    print("Browser closed")