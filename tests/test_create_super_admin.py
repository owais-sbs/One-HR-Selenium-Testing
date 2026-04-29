import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils import create_driver, login, dismiss_any_popup

BASE_URL = "http://localhost:3000"
USERNAME = "kiran@admin.com"
PASSWORD = "123456"
LOGIN_ROLE = "super_admin"
SUPER_ADMIN_NAME = "Test Super Admin"

timestamp = int(time.time())
SUPER_ADMIN_EMAIL = f"superadmin{timestamp}@test.com"
SUPER_ADMIN_PASSWORD = "123456"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=30)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/super-admins")
    print("Super Admin page opened")

    add_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add Super Admin')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", add_button)
    print("Add Super Admin clicked")

    wait.until(EC.presence_of_element_located((By.ID, "sa-name"))).send_keys(SUPER_ADMIN_NAME)
    print("Name entered")

    wait.until(EC.presence_of_element_located((By.ID, "sa-email"))).send_keys(SUPER_ADMIN_EMAIL)
    print("Dynamic email used:", SUPER_ADMIN_EMAIL)

    wait.until(EC.presence_of_element_located((By.ID, "sa-password"))).send_keys(SUPER_ADMIN_PASSWORD)
    print("Password entered")

    wait.until(EC.presence_of_element_located((By.ID, "sa-confirm"))).send_keys(SUPER_ADMIN_PASSWORD)
    print("Confirm password entered")

    create_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Create Super Admin')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", create_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", create_button)
    print("Create Super Admin clicked")

    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{SUPER_ADMIN_EMAIL}')]"))
        )
        print("Super Admin created successfully")
    except TimeoutException:
        print("Super Admin creation verification failed")

    time.sleep(5)

except Exception as e:
    print("Test failed:", e)
    screenshot_path = SCREENSHOT_DIR + f"/error_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved:", screenshot_path)

finally:
    driver.quit()
    print("Browser closed")
