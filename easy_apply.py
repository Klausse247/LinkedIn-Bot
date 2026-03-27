import time
import yaml
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CONFIG_PATH = Path(__file__).with_name("config.yaml")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_driver(cfg):
    opts = Options()
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-background-timer-throttling")
    opts.add_argument("--disable-backgrounding-occluded-windows")
    opts.add_argument("--disable-renderer-backgrounding")
    opts.add_argument("--log-level=0")
    opts.add_argument("--enable-logging")
    opts.add_argument("--v=1")  # Verbose logging
    
    if cfg["selenium"].get("headless", False):
        opts.add_argument("--headless=new")
    profile_dir = cfg["selenium"].get("profile_dir")
    if profile_dir:
        opts.add_argument(f"--user-data-dir={profile_dir}")
        # opts.add_argument("--no-sandbox")
        # opts.add_argument("--disable-dev-shm-usage")
        # opts.add_argument("--disable-gpu")
        # opts.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    return driver

def main():
    cfg = load_config()
    driver = get_driver(cfg)
    try:
        driver.get("https://www.linkedin.com/jobs/")
        time.sleep(5)
        # TODO: perform search, filter Easy Apply, loop jobs, apply
        input("Check you are logged in, then press Enter...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
