import time
import random
from datetime import datetime, timedelta
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import logging

# Set up logging
logging.basicConfig(filename='punch_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define your credentials
COMPANY_CODE = ""
EMPLOYEE_CODE = ""
PASSWORD = ""

# URL of the login page
LOGIN_URL = "https://selfservice.pockethrms.com/"

# Set up the Selenium WebDriver (using Chrome in headless mode)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to log in and click the Punch button
def login_and_punch():
    logging.info("Starting login and punch process")
    driver = setup_driver()
    try:
        # Open the login page
        driver.get(LOGIN_URL)
        logging.info("Opened login page")

        # Wait for the page to load
        time.sleep(6)

        # Enter Company Code
        company_code_field = driver.find_element(By.ID, "CompanyCode")
        company_code_field.send_keys(COMPANY_CODE)
        logging.info("Entered Company Code")

        # Enter Employee Code
        employee_code_field = driver.find_element(By.ID, "EmployeeCode")
        employee_code_field.send_keys(EMPLOYEE_CODE)
        logging.info("Entered Employee Code")

        # Enter Password
        password_field = driver.find_element(By.ID, "Password")
        password_field.send_keys(PASSWORD)
        logging.info("Entered Password")

        # Click the Sign In button
        sign_in_button = driver.find_element(By.XPATH,
                                             "//input[@type='submit' and @value='SIGN IN' and contains(@class, 'b-button-sumbit')]")
        sign_in_button.click()
        logging.info("Clicked Sign In button")

        # Wait for the dashboard to load
        time.sleep(5)

        # Find and click the Punch button
        punch_button = driver.find_element(By.ID, "btnPunch")
        punch_button.click()
        logging.info("Clicked Punch button")

        # Wait for a moment to ensure the action is completed
        time.sleep(5)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()
        logging.info("Browser closed")

# Function to schedule the tasks
def schedule_tasks():
    # Get current date in IST
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    today = now.date()

    # Schedule the morning punch (11:00 AM to 11:30 AM IST)
    morning_start_time = datetime.combine(today, datetime.strptime("11:00", "%H:%M").time(), tzinfo=ist)
    morning_end_time = datetime.combine(today, datetime.strptime("11:30", "%H:%M").time(), tzinfo=ist)

    # Generate a random time for the morning punch
    morning_time_diff = (morning_end_time - morning_start_time).seconds
    morning_random_seconds = random.randint(0, morning_time_diff)
    morning_random_time = morning_start_time + timedelta(seconds=morning_random_seconds)
    morning_random_time_str = morning_random_time.strftime("%H:%M")
    logging.info(f"Scheduled morning punch to run at {morning_random_time_str} IST")

    # Schedule the morning task
    schedule.every().day.at(morning_random_time_str).do(login_and_punch)

    # Schedule the evening punch (8:30 PM to 9:00 PM IST)
    evening_start_time = datetime.combine(today, datetime.strptime("20:00", "%H:%M").time(), tzinfo=ist)
    evening_end_time = datetime.combine(today, datetime.strptime("20:30", "%H:%M").time(), tzinfo=ist)

    # Generate a random time for the evening punch
    evening_time_diff = (evening_end_time - evening_start_time).seconds
    evening_random_seconds = random.randint(0, evening_time_diff)
    evening_random_time = evening_start_time + timedelta(seconds=evening_random_seconds)
    evening_random_time_str = evening_random_time.strftime("%H:%M")
    logging.info(f"Scheduled evening punch to run at {evening_random_time_str} IST")

    # Schedule the evening task
    schedule.every().day.at(evening_random_time_str).do(login_and_punch)

    # Keep the script running to check for scheduled tasks
    while True:
        # Get the current time in IST
        current_time = datetime.now(ist)

        # Run any pending scheduled tasks
        schedule.run_pending()

        # If the current time is past 9:00 PM, exit the loop
        if current_time.time() > evening_end_time.time():
            logging.info("Evening time window has passed. Exiting.")
            break

        # Sleep for 10 seconds to avoid high CPU usage
        time.sleep(10)

# Run the script
if __name__ == "__main__":
    logging.info("Starting script...")
    schedule_tasks()
