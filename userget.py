from twikit import Client
import asyncio
from typing import Union, List
import time
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = Client('en-US')

USERNAME = os.getenv('USERNAME')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
async def login():
    try:
        
        client.load_cookies('cookies.json')
        print('cookie loaded successfully')
    except:
        
        await client.login(
            auth_info_1=USERNAME ,
            auth_info_2=EMAIL,
            password=PASSWORD
            )
        client.save_cookies('cookies.json')
        print('logged in with password')
asyncio.run(login())

async def GUD(list_of_users_id):

    if isinstance(list_of_users_id,str):
        list_of_users_id=[list_of_users_id]
    user_dict={}
    for user_id in list_of_users_id:
        try:
            user=await client.get_user_by_screen_name(user_id)
            user_info={
                "idd" :user.id,
                "name":user.name,
                "created_at":user.created_at,
                "location":user.location,
                "description":user.description,
                "can_dm":user.can_dm,
                "can_media_tag": user.can_media_tag,
                "verified": user.verified,
                "want_retweets": user.want_retweets,
                "followers_count": user.followers_count,
                "fast_followers_count":user.fast_followers_count,
                "normal_followers_count":user.normal_followers_count,
                "following_count":user.following_count,
                "statuses_count":user.statuses_count,
                "media_count":user.media_count,
                "withheld_in_countries":user.withheld_in_countries,
                "follower_of":[]
            }
            user_dict[user_id]=user_info
        except Exception as e:
            print(f"error getting user with ID : {user_id} with exception {e}")
            continue
    return user_dict


async def get_followers(list_of_users_id:Union[str, List[str]]) -> Union[str, List[str]]:
    #can also take user id as input
    if isinstance(list_of_users_id,str):
        list_of_users_id=[list_of_users_id]
    user_dict={}
    for user_id in list_of_users_id:

        try:
            user= await client.get_user_by_screen_name(user_id)

        except Exception as e:
            print(f"error getting user with ID : {user_id} with exception {e}")
            continue
        try :
            if user.screen_name==user_id:
                followers = await user.get_followers(150)
                for follower in followers:
                    follower_info={
                        "idd" :follower.id,
                        "name":follower.name,
                        "created_at":follower.created_at,
                        "location":follower.location,
                        "description":follower.description,
                        "can_dm":follower.can_dm,
                        "can_media_tag": follower.can_media_tag,
                        "verified": follower.verified,
                        "want_retweets": follower.want_retweets,
                        "followers_count": follower.followers_count,
                        "fast_followers_count":follower.fast_followers_count,
                        "normal_followers_count":follower.normal_followers_count,
                        "following_count":follower.following_count,
                        "statuses_count":follower.statuses_count,
                        "media_count":follower.media_count,
                        "withheld_in_countries":follower.withheld_in_countries,
                        "follower_of":[user_id]
                    }
                    if follower.screen_name in user_dict.keys():
                        user_dict[follower.screen_name]["follower_of"]=user_dict[follower.screen_name]["follower_of"]+[user_id]
                    else:
                        user_dict[follower.screen_name]=follower_info
        except Exception as e:
            print(f"error getting followers for user with ID : {user_id} with exception {e}")
            continue
    return user_dict
async def get_posts(list_of_users_id):
    tweets_list=[]
    if isinstance(list_of_users_id,str):
        list_of_users_id=[list_of_users_id]
    for user_id in list_of_users_id:
        try:
            user= await client.get_user_by_screen_name(user_id)
        except Exception as e:
            print(f"error getting user with ID : {user_id} with exception {e}")
            continue
        tweets= await user.get_tweets('Tweets',20)
        for tweet in tweets:
            tweets_list.append(f"https://x.com/{tweet.user.screen_name}/status/{tweet.id}")
    return tweets_list


    



if __name__ == "__main__":
    web3_twitter_profiles=['web3isgreat', 'molly0xFFF', 'smdiehl', 'rufuspollock', 'troll_lock', 'CasPiancey', 'BennettTomlin', 'SilvermanJacob', 'ben_mckenzie', 'doctorow']

    asyncio.run(login())
    startt=time.time()
    users_followers=asyncio.run(get_posts(web3_twitter_profiles))
    endt=time.time()
    print(users_followers)
    print(f"get_followers Execution time: {endt - startt:.4f} seconds")
    with open('crypto_accounts.json' , 'w') as file:
        json.dump(users_followers,file,indent=4)





    

