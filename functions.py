from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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


def setup_driver(driver_path):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')  
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage')  
    chrome_options.add_argument('--disable-extensions')  
    chrome_options.add_argument('--disable-logging')  
    chrome_options.add_argument('--log-level=3')  
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--disable-software-rasterizer')  
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-xss-auditor')  
    chrome_options.add_argument('--disable-webgl')  
    chrome_options.add_argument('--disable-gl-extensions')  
    chrome_options.page_load_strategy = 'eager'  

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(0.1)
    
    return driver


def process_all_users(csv_file, driver_path, max_workers=3):
    users_df = pd.read_csv(csv_file)
    users_list = users_df.to_dict('records')
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        all_results = list(executor.map(lambda user_data: process_user(user_data, driver_path), users_list))
        
    flattened_results = [item for sublist in all_results for item in sublist]
    final_df = pd.DataFrame(flattened_results)
    
    # Save results
    final_df.to_csv("results.csv", index=False)
    print(f"Results saved to results.csv")
    return final_df


def process_user(user_data, driver_path):
    driver = setup_driver(driver_path)
    roll_no, email, dob = user_data['roll_no'], user_data['email'], user_data['dob']
    results = []
    
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
            (By.LINK_TEXT, "Click to view Results: October 2024")))
        driver.execute_script("arguments[0].click();", results_link)
        
        # Handle new window/tab
        new_window = wait.until(lambda d: len(d.window_handles) > 1)
        if new_window:
            driver.switch_to.window(driver.window_handles[-1])
        
        # Get results table
        table = wait.until(EC.presence_of_element_located((By.ID, "exam_score")))
        results = extract_table_data(roll_no, table)
        
        print(f"Successfully processed {email}")
        
    except Exception as e:
        print(f"Error processing {email}: {str(e)}")
        
    finally:
        driver.quit()
        return results
