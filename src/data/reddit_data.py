# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import logging
import datetime
import requests
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger("Reddit")
project_dir = "./"


subs_of_interest = ["CryptoCurrency"]

def authenticate_reddit():
    """
        Authenticate Script to be able to access the reddit API
    """
    logger.info("Authenticating reddit ... Fetching username and password ...")

    auth = requests.auth.HTTPBasicAuth(os.environ.get("APP_ID"), os.environ.get("APP_SECRET"))

    reddit_user = os.environ.get("REDDIT_USER") if (os.environ.get("REDDIT_USER") != None) else input("Reddit Username: ")
    reddit_password = os.environ.get("REDDIT_PASS") if (os.environ.get("REDDIT_PASS") != None) else input("Reddit Password: ")

    data = {
    'grant_type': 'password',
    'username': reddit_user,
    'password': reddit_password
    }

    headers = {'User-Agent': 'SYSC_4906/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    logger.info(res.status_code)

    if(res.status_code == 200):
        logger.info("Authentication was a success")
        return res.json()['access_token']
    else:
        raise Exception("Authentication Failed")

def restructure_subreddit_data(reddit_data):
    """
        Restructure data from a subbreddit
    """

    subreddit_data_slice = pd.DataFrame()
    post_time = -1
    # loop through each post pulled from res and append to df
    for post in reddit_data['data']['children']:
        # identify time
        last_post_time = post['data']['created_utc'] 

        subreddit_data_slice = subreddit_data_slice.append({
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'created_utc': datetime.datetime.fromtimestamp(post['data']['created_utc']).strftime("%Y-%m-%d"),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)
    
    last_row = subreddit_data_slice.iloc[len(subreddit_data_slice)-1]
    after = last_row['kind'] + '_' + last_row['id']

    return subreddit_data_slice, after, last_post_time

def pull_subreddit(subreddit_name, authentication, days_ago = 1):
    """
        pull all posts from a subbreddit between now and the specified amount of days prior to pull too
    """
    params = {'limit': 100}
    subreddit_data = pd.DataFrame()
    
    try:
        for i in range(10):
            res = requests.get("https://oauth.reddit.com/r/{}/new".format(subreddit_name),
                            headers=authentication,
                            params=params)

            if(res.status_code == 200):
                logger.info("Success pulling data from {}".format(subreddit_name))

                subreddit_slice, last_id, last_post = restructure_subreddit_data(res.json())

                subreddit_data = subreddit_data.append(subreddit_slice, ignore_index=True)
                logger.info("Last data pull was from: {}".format(time.ctime(last_post)))

                if((int(time.time()) - int(last_post)) >= days_ago*86400 ): # time difference is more than a certain span of seconds (86400 secs in a day)
                    # Break out by throwing a 'Done' error
                    raise Exception("Done")
                else:
                    # set the last id parameters to know where we should pull from next
                    params["after"] = last_id

            else:
                logger.error("Status code {} recieved".format(res.status_code))
                raise Exception("Failure pulling data")
            
            # Wait 2 seconds before next call to reddit API
            time.sleep(1)

    except Exception as e:
        logger.error(e)

    return subreddit_data
    

def reddit():
    """ 
        Steps to pull data from reddit
    """
    # Get authentication token from reddit
    try:
        access_token = authenticate_reddit()
        logger.info("Authentication Token is: {}".format(access_token))
    except Exception as e:
        logger.error(e)
        return 400

    # Create the header to be used in future get requests
    authentication_header = {'User-Agent': 'SYSC_4906/0.0.1', 'Authorization' : 'bearer {}'.format(access_token)}
   
    subreddits_to_explore = json.load(open("{}/src/data/reddit_config.json".format(project_dir)))

    for this_subreddit in subreddits_to_explore["subreddits"]:
        try:
            logger.info("Attempting to fetch data from r/{}".format(this_subreddit["sub_name"]))

            subreddit_pull = pull_subreddit(this_subreddit["sub_name"], authentication_header, 1)

            logger.info("Saving r/{} data to: {}/data/raw/reddit/r_{}.json".format(this_subreddit["sub_name"], project_dir, this_subreddit["sub_name"]))

            subreddit_pull.to_json("{}/data/raw/reddit/r_{}.json".format(project_dir, this_subreddit["sub_name"]), orient="index")

        except Exception as e:
            logger.warning(e)
            logger.error("Unable to pull data from the {} subreddit".format(this_subreddit["sub_name"]))

    return 200
    


if __name__ == '__main__':
    try:
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            filemode='w', filename="reddit_data_logs.log")

        project_dir = Path(__file__).resolve().parents[2]

        logger.info("Running in {}".format(project_dir))

        # Load in environment variables from .env
        load_dotenv(find_dotenv())

        status = reddit()

        logger.info(status)
    except Exception as e:
        logger.error(e)


