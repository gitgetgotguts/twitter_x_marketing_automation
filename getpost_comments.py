from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import asyncio
from bs4 import BeautifulSoup


import userget
def loadx_cookies():
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceMetrics": 
    { "width": 500, "height": 9999, "pixelRatio": 3.0 }})
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    url="https://x.com"
    driver.get(url)
    # Load login session cookies from a JSON file
    with open('login_cookies.json', 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver

    
def get_users_from_url(url,driver):


    # Reload the URL with the cookies
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    users_set = set()
    # Scroll to the bottom of the page to load more elements
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new elements to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        usersoup = soup.select("div.css-146c3p1.r-dnmrzs.r-1udh08x.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-1b43r93.r-hjklzo.r-16dba41.r-18u37iz.r-1wvb978")
        for u in usersoup:
            users_set.add(u.text)

        if new_height == last_height:
            break
        last_height = new_height

    
    users_list=[user[1:] for user in users_set]
    return set(users_list)

if __name__ == "__main__":
    driver=loadx_cookies()
    DATA=asyncio.run(userget.GUD(get_users_from_url("https://x.com/mrsiipa/status/1866862186200698999",driver)))
    with open('crypto_accounts_from_post.json' , 'w') as file:
        json.dump(DATA,file,indent=4)