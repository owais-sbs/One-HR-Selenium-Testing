import time
from utils import create_driver, login, dismiss_any_popup, print_error_details, save_failure_artifacts

BASE_URL = "http://localhost:3000"
USERNAME = "zafar@onehr.com"
PASSWORD = "123456"
LOGIN_ROLE = "company_admin"

driver, wait = create_driver(timeout=20)

try:
    print("Opening login page...")
    login(driver, wait, BASE_URL, USERNAME, PASSWORD, preferred_role=LOGIN_ROLE)
    dismiss_any_popup(driver)

    print("Login SUCCESS")
    print("Dashboard URL:", driver.current_url)
    time.sleep(5)

except Exception as e:
    print_error_details(e, driver)
    save_failure_artifacts(driver)

finally:
    driver.quit()
    print("Browser closed")
