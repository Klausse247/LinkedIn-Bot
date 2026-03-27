from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

opts = Options()
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service()  # Auto‑finds chromedriver
driver = webdriver.Chrome(service=service, options=opts)
driver.get("https://www.google.com")
print("✅ Success! Title:", driver.title)
input("Press Enter to close...")
driver.quit()