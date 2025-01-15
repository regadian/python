from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


# Error messages
LOCKED_ERROR_MSG = "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour."
#INVALID_CREDENTIALS_ERROR_MSG = "Warning: No match for E-Mail Address and/or Password."

def login(driver, username = None, password = None):
    """performs login and returns error element"""
    button_login = driver.find_element(By.CSS_SELECTOR, "input[class='btn btn-primary']")
    button_login.click()
    return wait_for_alert(driver)

def wait_for_alert(driver):
    """ Waits for error message and returns it"""
    return WebDriverWait(driver, 10).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
      )

def fill_in_login_details(driver, username, password):
    """Fill the username and password field before login."""
    username_field = WebDriverWait(driver,10).until(
         EC.visibility_of_element_located((By.ID,"input-email"))
      )
    username_field.clear()
    username_field.send_keys(username)
    
    password_field = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.ID,"input-password"))
      )
    password_field.clear()
    password_field.send_keys(password)

# Set options to initialize the webdriver.
chrome_options = Options()
#chrome_options.add_argument('--headless=new') # optional: runs chrome in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


try:
     # Explicit driver initialization
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(10) #wait 10 seconds max for all selenium operations.

    # Open the login page
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

    # Test Case 1: Invalid login
    # Click the login button without filling the form
    alert_element_1 = login(driver)
    print(f"Alert HTML: {alert_element_1.get_attribute('outerHTML')}")
    
    # Assert the alert text for the locked account (test case 1)
    assert alert_element_1.text.strip() == LOCKED_ERROR_MSG, "Alert message does not match!"
    print("Test passed: Alert message verified successfully.")

    
    # Test Case 2: Invalid username and password (unregistered)
    # Fill the login form with unregistered credentials
    fill_in_login_details(driver, "invaliduser@example.com","invalidpassword123")
    # Click the login button again
    invalid_alert = login(driver)
    print(f"Invalid Alert HTML: {invalid_alert.get_attribute('outerHTML')}")
    time.sleep(3)
    # Assert the alert text for invalid login attempt (test case 2)
    assert invalid_alert.text.strip() == LOCKED_ERROR_MSG, "Alert message does not match for invalid login!"
    print("Test passed: Invalid login alert message verified successfully.")

except WebDriverException as e:
    print(f"WebDriver error: {e}")
except AssertionError as e:
    print(f"Assertion Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'driver' in locals() and driver:
        driver.quit()  # Quit the browser