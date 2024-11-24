from functions import*

DRIVER_PATH = r"D:\Tools\chromedriver-win64\chromedriver.exe"
CSV_FILE = "email.csv"

results = process_all_users(CSV_FILE, DRIVER_PATH, 10)