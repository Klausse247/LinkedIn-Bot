import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
USERNAME = os.environ.get("LINKEDIN_USERNAME")
PASSWORD = os.environ.get("LINKEDIN_PASSWORD")

if not USERNAME or not PASSWORD:
    print("Please set LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables.")
    exit(1)

opts = Options()
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service()  # Auto‑finds chromedriver
driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://linkedin.com/login")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

    driver.execute_script("arguments[0].value = '';", username_field)
    driver.execute_script("arguments[0].value = arguments[1];", username_field, USERNAME)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", username_field)
    
    driver.execute_script("arguments[0].value = '';", password_field)
    driver.execute_script("arguments[0].value = arguments[1];", password_field, PASSWORD)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", password_field)

    #print(f"DEBUG: Username var: '{USERNAME}' (length: {len(USERNAME)})") #Debugging line to check if USERNAME is correctly set and has the expected length. Remove or comment out in production.
    #print(f"DEBUG: Password var: '{PASSWORD}' (length: {len(PASSWORD)})") #Debugging line to check if PASSWORD is correctly set and has the expected length. Remove or comment out in production.
    
    # Submit
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    print("Logged in? Current URL:", driver.current_url)
    input("Press Enter to close...")

finally:
    driver.quit()