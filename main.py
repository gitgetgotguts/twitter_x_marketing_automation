#add a users list 
users_list=['web3isgreat', 'molly0xFFF', 'smdiehl', 'rufuspollock', 'troll_lock', 'CasPiancey', 'BennettTomlin', 'SilvermanJacob', 'ben_mckenzie', 'doctorow']
#this will return a csv from the users accounts
#if you have problems try running the twitter login and add your account credentials in a .env file

from userget import get_followers
from userget import login
import asyncio
from twikit import Client
import json
import time
import csv
import os
from dotenv import load_dotenv
from userget import login, get_followers, get_posts
from getpost_comments import get_users_from_url, loadx_cookies

# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv('USERNAME')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

client = Client('en-US')

asyncio.run(login())
users_followers=asyncio.run(get_followers(users_list))
recent_tweets=asyncio.run(get_posts(users_list))
driver=loadx_cookies()
users_set_name=set()
for link in recent_tweets:
    users_set_name.update(get_users_from_url(link,driver))
driver.close()
users_screen=list(users_set_name)
data=asyncio.run(get_followers(users_screen))
users_followers.update(data)
with open('FINAL.json' , 'w') as file:
    json.dump(users_followers, file)

import pandas as pd 
data=pd.read_json("FINAL.json")
data=data.T
data.set_index("idd",inplace=True)
data.to_excel("usersFINAL.xlsx")
    



