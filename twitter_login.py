import time
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



USERNAME = os.getenv('USERNAME')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(options=options)
url = "https://twitter.com/i/flow/login"
driver.get(url)

username = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
username.send_keys(EMAIL)
username.send_keys(Keys.ENTER)

password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

time.sleep(10)
# Save cookies to a JSON file
cookies = driver.get_cookies()
with open('login_cookies.json', 'w') as file:
    json.dump(cookies, file)

# Close the browser
driver.quit()