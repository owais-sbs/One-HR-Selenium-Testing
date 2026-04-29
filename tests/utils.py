from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import time
import os
import traceback


ROLE_LABELS = {
    "super_admin": "Super Admin",
    "company_admin": "Company Admin",
    "finance_manager": "Finance Manager",
    "hr_manager": "HR Manager",
    "department_manager": "Department Manager",
    "employee": "Employee",
}

ROLE_PRIORITY = [
    "super_admin",
    "company_admin",
    "finance_manager",
    "hr_manager",
    "department_manager",
]


def get_chrome_options():
    options = Options()
    options.page_load_strategy = "eager"

    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument(
        "--disable-features="
        "PasswordLeakDetection,"
        "PasswordManagerOnDesktop,"
        "PasswordManagerOnboarding,"
        "PasswordManagerLeakDetection,"
        "PasswordGeneration,"
        "InsecureDownloadWarnings,"
        "PasswordCheck"
    )

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "credentials_enable_autosignon": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "password_manager_enabled": False,
        "browser.safebrowsing.enabled": False,
        "browser.safebrowsing.malware.enabled": False,
        "profile.content_settings.exceptions.clipboard": {},
    })

    return options


def create_driver(timeout=30):
    options = get_chrome_options()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_window_size(1920, 1080)
    wait = WebDriverWait(driver, timeout)
    return driver, wait


def dismiss_any_popup(driver, short_wait=2):
    """
    Attempt to dismiss any unexpected popups, alerts, or overlays.
    Call this at critical junctures to prevent browser popups from
    blocking test execution.
    """
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except Exception:
        pass

    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body.click()
    except Exception:
        pass

    try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except Exception:
        pass

    dismiss_selectors = [
        "//button[contains(., 'Close')]",
        "//button[contains(., 'Dismiss')]",
        "//button[contains(., 'Cancel')]",
        "//button[contains(., 'No')]",
        "//button[contains(., 'Not now')]",
        "//button[contains(., 'Never')]",
        "//button[contains(., 'Skip')]",
        "//button[contains(., 'Got it')]",
        "//button[contains(., 'OK')]",
        "//button[contains(., 'Ok')]",
        "//button[contains(., 'Understand')]",
        "//button[contains(., 'Accept')]",
        "//button[contains(., 'Agree')]",
        "//button[contains(., 'No thanks')]",
        "//button[contains(., 'Maybe later')]",
        "//button[@aria-label='Close']",
        "//button[@aria-label='Dismiss']",
        "//div[@role='dialog']//button[contains(., 'Close')]",
        "//div[@role='dialog']//button[contains(., 'Cancel')]",
        "//div[@role='dialog']//button[contains(., 'OK')]",
    ]

    for selector in dismiss_selectors:
        try:
            for element in driver.find_elements(By.XPATH, selector):
                if element.is_displayed() and element.is_enabled():
                    driver.execute_script("arguments[0].click();", element)
                    return
        except Exception:
            continue


def normalize_role(role):
    if not role:
        return None

    normalized = role.strip().lower().replace(" ", "_")
    return normalized or None


def role_label(role):
    normalized = normalize_role(role)
    if not normalized:
        return None
    return ROLE_LABELS.get(normalized, role)


def set_controlled_input(driver, element, value):
    """
    Update a controlled React input so onChange handlers fire.
    """
    driver.execute_script(
        """
        const el = arguments[0];
        const nextValue = arguments[1];
        const setter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype,
          "value"
        ).set;
        setter.call(el, nextValue);
        el.dispatchEvent(new Event("input", { bubbles: true }));
        el.dispatchEvent(new Event("change", { bubbles: true }));
        """,
        element,
        value,
    )


def click_visible_element(driver, elements):
    for element in elements:
        if element.is_displayed() and element.is_enabled():
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            driver.execute_script("arguments[0].click();", element)
            return True
    return False


def handle_role_selection(driver, wait, preferred_role=None):
    """
    Handle the role selection page that may appear after login.
    Tries multiple role button patterns and the Continue button.
    """
    preferred_label = role_label(preferred_role)
    role_labels_to_try = []
    if preferred_label:
        role_labels_to_try.append(preferred_label)
    for role_key in ROLE_PRIORITY:
        label = ROLE_LABELS[role_key]
        if label not in role_labels_to_try:
            role_labels_to_try.append(label)

    role_page_detected = False

    try:
        short_wait = WebDriverWait(driver, 8)
        short_wait.until(
            lambda d: d.find_elements(
                By.XPATH, "//h2[contains(., 'Select your role')]"
            )
            or d.find_elements(
                By.XPATH, "//p[contains(., 'Choose one role to continue')]"
            )
            or d.find_elements(By.XPATH, "//button[.//span[contains(., 'Admin')] or .//span[contains(., 'Manager')] or .//span[normalize-space()='Employee']]")
        )
        role_page_detected = True
        print("Role selection page detected")

        selected_role = None
        for label in role_labels_to_try:
            if click_visible_element(
                driver,
                driver.find_elements(
                    By.XPATH,
                    f"//button[.//span[normalize-space()='{label}'] or normalize-space()='{label}' or contains(normalize-space(.), '{label}')]",
                ),
            ):
                selected_role = label
                print("Role clicked:", label)
                break

        if not selected_role:
            for button in driver.find_elements(By.XPATH, "//button"):
                text = (button.text or "").strip()
                if text in role_labels_to_try and click_visible_element(driver, [button]):
                    selected_role = text
                    print("Role clicked via fallback:", text)
                    break

        continue_btn = short_wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
        )
        driver.execute_script("arguments[0].click();", continue_btn)
        print("Continue clicked on role page")

    except TimeoutException:
        if role_page_detected:
            print("Role selection page detected but no actionable controls were found")
        else:
            print("Role selection not required")


def login(driver, wait, base_url, username, password, preferred_role=None):
    """
    Robust login with automatic role selection and popup dismissal.
    Uses JavaScript-based form filling to bypass browser password
    detection heuristics that trigger popups.
    """
    driver.get(base_url)
    dismiss_any_popup(driver)

    username_input = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    set_controlled_input(driver, username_input, username)

    password_input = wait.until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    set_controlled_input(driver, password_input, password)

    dismiss_any_popup(driver)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )

    try:
        login_button.click()
    except UnexpectedAlertPresentException:
        try:
            driver.switch_to.alert.dismiss()
        except Exception:
            pass
        driver.execute_script("arguments[0].click();", login_button)

    print("Login submitted")

    dismiss_any_popup(driver)
    handle_role_selection(driver, wait, preferred_role=preferred_role)
    dismiss_any_popup(driver)

    wait.until(EC.url_contains("/dashboard"))
    print("Dashboard opened")


def save_failure_artifacts(driver, screenshot_dir="screenshots", html_dir=None):
    """
    Save screenshot and page HTML on test failure.
    """
    timestamp = int(time.time())

    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = f"{screenshot_dir}/error_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved:", screenshot_path)

    if html_dir:
        os.makedirs(html_dir, exist_ok=True)
        html_path = f"{html_dir}/error_page_{timestamp}.html"
    else:
        html_path = f"{screenshot_dir}/page_{timestamp}.html"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("HTML saved:", html_path)


def print_error_details(e, driver):
    """
    Print detailed error info including URL, title, and stack trace.
    """
    print("\n================ ERROR DETAILS ================\n")
    print("Error message:", str(e))
    print("\nCurrent URL:", driver.current_url)
    print("\nPage title:", driver.title)
    print("\nStacktrace:")
    traceback.print_exc()
