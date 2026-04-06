import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
USERNAME = os.environ.get("LINKEDIN_USERNAME") # this is to grab the username from the .env file 
PASSWORD = os.environ.get("LINKEDIN_PASSWORD") #This is to grab the password from the .env file

if not USERNAME or not PASSWORD:
    print("Please set LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables.") #to check if the username and password are set in the environment variables.
    exit(1)

opts = Options()
opts.add_argument("--no-sandbox") 
opts.add_argument("--disable-dev-shm-usage") # These options are often needed for running Chrome in certain environments, especially in containers or headless mode. They help prevent issues related to resource limits and sandboxing that can cause Chrome to crash or fail to start.

service = Service()  # Auto‑finds chromedriver
driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver, 15)


def push_easy_apply():
    try:
            easy_apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-apply-button"))) # Wait for the "Easy Apply" button to be clickable before trying to click it. This ensures that the page has loaded the necessary elements and that the button is interactable before we attempt to click it.
            easy_apply_button.click()
            print("Clicked 'Easy Apply' button.")
    except Exception as e:
            print("Error clicking 'Easy Apply' button:", e)
    
    
try:
        driver.get("https://linkedin.com/login")
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username"))) # Wait for the username field to be present before trying to interact with it. This ensures that the page has loaded the necessary elements before we attempt to set the values.
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password"))) # Wait for the password field to be present before trying to interact with it. This ensures that the page has loaded the necessary elements before we attempt to set the values.

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
        elif "sign in" not in page_source and "incorrect password" not in page_source:
            print("✅ Login looks successful.")

            driver.get("https://www.linkedin.com/jobs/search-results/?currentJobId=4388933557&keywords=cyber%20security%20Engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&referralSearchId=MVTytOam%2BX6veRRsqEpqFQ%3D%3D&geoId=90000077&distance=0.0&f_AL=true&f_SAL=f_SA_id_227001%3A276001%2C277001%24f_SA_id_226001%3A272015")

            push_easy_apply()
        else:
            print("❌ Login may have failed.")

        input("Press Enter to close...")

finally:
        driver.quit()
