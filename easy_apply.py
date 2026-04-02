import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    print("Logged in? Current URL:", driver.current_url)
    input("Press Enter to close...")
finally:
    driver.quit()
