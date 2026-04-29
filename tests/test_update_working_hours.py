import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "abdulhameed@opbs.com"
PASSWORD = "123456"
LOGIN_ROLE = "hr_manager"
START_TIME = "09:30"
END_TIME = "18:30"
BREAK_MINUTES = "60"
GRACE_MINUTES = "15"

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

driver, wait = create_driver(timeout=40)

try:
    print("Opening login page")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    driver.get("http://localhost:3000/settings/working-hours")
    print("Working Hours page opened")
    time.sleep(2)

    print("Selecting working days")
    monday_checkbox = wait.until(EC.presence_of_element_located((By.ID, "Monday")))
    tuesday_checkbox = driver.find_element(By.ID, "Tuesday")

    if not monday_checkbox.is_selected():
        driver.execute_script("arguments[0].click();", monday_checkbox)
    if not tuesday_checkbox.is_selected():
        driver.execute_script("arguments[0].click();", tuesday_checkbox)
    print("Working days selected")

    start_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='time'][1]")))
    start_input.clear()
    start_input.send_keys(START_TIME)
    print("Start time set")

    end_input = driver.find_element(By.XPATH, "(//input[@type='time'])[2]")
    end_input.clear()
    end_input.send_keys(END_TIME)
    print("End time set")

    break_input = driver.find_element(By.XPATH, "(//input[@type='number'])[1]")
    break_input.clear()
    break_input.send_keys(BREAK_MINUTES)
    print("Break minutes set")

    grace_input = driver.find_element(By.XPATH, "(//input[@type='number'])[2]")
    grace_input.clear()
    grace_input.send_keys(GRACE_MINUTES)
    print("Grace minutes set")

    save_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save Changes')]"))
    )
    driver.execute_script("arguments[0].click();", save_button)
    print("Save Changes clicked")

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Working hours saved')]"))
    )
    print("Working hours saved successfully")
    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver, SCREENSHOT_DIR)

finally:
    driver.quit()
    print("Browser closed")
