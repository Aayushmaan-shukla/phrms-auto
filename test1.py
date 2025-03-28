import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define your credentials
COMPANY_CODE = "EPS"
EMPLOYEE_CODE = "85"
PASSWORD = "8528122002"  # Replace with the actual password

# URL of the login page
LOGIN_URL = "https://selfservice.pockethrms.com/"

# Set up the Selenium WebDriver (using Chrome)
def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Function to log in and click the Punch button
def login_and_punch():
    driver = setup_driver()
    try:
        # Open the login page
        driver.get(LOGIN_URL)
        print("Opened login page")

        # Wait for the page to load
        time.sleep(10)

        # Enter Company Code
        company_code_field = driver.find_element(By.ID, "CompanyCode")
        company_code_field.send_keys(COMPANY_CODE)
        print("Entered Company Code")

        # Enter Employee Code
        employee_code_field = driver.find_element(By.ID, "EmployeeCode")
        employee_code_field.send_keys(EMPLOYEE_CODE)
        print("Entered Employee Code")

        # Enter Password
        password_field = driver.find_element(By.ID, "Password")
        password_field.send_keys(PASSWORD)
        print("Entered Password")

        # Click the Sign In button
        sign_in_button = driver.find_element(By.XPATH,
                                             "//input[@type='submit' and @value='SIGN IN' and contains(@class, 'b-button-sumbit')]")
        sign_in_button.click()
        print("Clicked Sign In button")



        # Wait for the dashboard to load
        time.sleep(8)

        # Find and click the Punch button
        punch_button = driver.find_element(By.ID, "btnPunch")
        punch_button.click()
        print("Clicked Punch button")

        # Wait for a moment to ensure the action is completed
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

# Run the script immediately
if __name__ == "__main__":
    print("Starting script...")
    login_and_punch()