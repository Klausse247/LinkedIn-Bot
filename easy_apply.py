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
    
    WebDriverWait(driver, 20).until(lambda d: d.current_url != "https://www.linkedin.com/login") # Wait until URL changes from login page, indicating a successful login or redirection to a checkpoint.
    current_url = driver.current_url
    page_source = driver.page_source.lower()

    print("Current URL:", current_url)

    if "checkpoint" in current_url or "challenge" in current_url:
        print("⚠️ LinkedIn wants verification/checkpoint.")
    elif "/feed" in current_url or "/in/" in current_url or "linkedin.com/" in current_url:
        if "sign in" not in page_source and "incorrect password" not in page_source:
            print("✅ Login looks successful.")
        else:
            print("❌ Login may have failed.")
    else:
        print("⚠️ Unknown post-login state.")

    input("Press Enter to close...")
finally:
    driver.quit()