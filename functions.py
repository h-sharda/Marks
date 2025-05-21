from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def extract_table_data(roll_no, table):
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    
    for row in rows[1:]:  
        try:
            columns = row.find_elements(By.TAG_NAME, "td")
            if columns:
                data.append({
                    "Roll Number": roll_no,
                    "Name": columns[1].text,
                    "Course Name": columns[2].text,
                    "Assignment (25)": columns[3].text,
                    "Exam (75)": columns[4].text,
                    "Total (100)": columns[5].text
                })
        except Exception:
            continue
            
    return data


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def process_all_users(input_file, output_file):
    users_df = pd.read_csv(input_file)
    users_list = users_df.to_dict('records')
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        all_results = list(executor.map(lambda user_data: process_user(user_data), users_list))
        
    flattened_results = [item for sublist in all_results for item in sublist]
    final_df = pd.DataFrame(flattened_results)
    
    # Save results
    final_df.to_csv(output_file, index=False)
    print("\n\n------------------------------------------")
    print("Results saved to: ", output_file)
    print("------------------------------------------\n\n")
    return final_df


def process_user(user_data):
    driver = setup_driver()
    roll_no, email, dob = user_data['roll_no'], user_data['email'], user_data['dob']
    results = []

    temp = dob.split('-')
    dob = temp[2] + '-' + temp[1] + '-' + temp[0]
    
    try:
        # Navigate and login
        driver.get("https://internalapp.nptel.ac.in/B2C/")
        
        # Use WebDriverWait for more reliable element interaction
        wait = WebDriverWait(driver, 10)
        
        email_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Email ID']")))
        email_input.send_keys(email)
        
        password_input = driver.find_element(
            By.XPATH, "//input[@placeholder='Password (Format: YYYY-MM-DD)']")
        password_input.send_keys(dob, Keys.RETURN)
        
        # Click results link
        results_link = wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Click to view Results: April 2025")))
        driver.execute_script("arguments[0].click();", results_link)
        
        # Handle new window/tab
        new_window = wait.until(lambda d: len(d.window_handles) > 1)
        if new_window:
            driver.switch_to.window(driver.window_handles[-1])
        
        # Get results table
        table = wait.until(EC.presence_of_element_located((By.ID, "exam_score")))
        results = extract_table_data(roll_no, table)
        
        print("Successfully processed ", email)
        
    except Exception as e:
        print("Error processing ", email)
        
    finally:
        driver.quit()
        return results
