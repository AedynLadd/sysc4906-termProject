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
#from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger("Reddit")
project_dir = "./"

def restructure_subreddit_data(reddit_data):
    """
        Restructure data from a subbreddit
    """
    subreddit_data_slice = pd.DataFrame()
    last_post_time = -1
    # loop through each post pulled from res and append to df
    for post in reddit_data['data']:
        # identify time
        last_post_time = post['created_utc'] 
        try:
            subreddit_data_slice = subreddit_data_slice.append({
                'title': post['title'],
                'subreddit': post['subreddit'],
                'selftext': post['selftext'],
                'score': post['score'],
                'created_utc': datetime.datetime.fromtimestamp(post['created_utc']).strftime("%Y-%m-%d")
            }, ignore_index=True)
        except Exception as e:
            print("skipping post")

    return subreddit_data_slice, last_post_time

def getPushshiftData(time_start, subreddit):
    url = 'https://api.pushshift.io/reddit/search/submission/?size=500&before={}&subreddit={}'.format(time_start, subreddit)
    
    r = requests.get(url)
    data = r.json()
    return restructure_subreddit_data(data)


def pull_subreddit_data(subreddit_name, days_ago = 1):
    """
        pull all posts from a subreddit between now and the specified amount of days prior
    """
    collected_data = pd.DataFrame()
    last_post = int(time.time())
    try:
        for i in range(0,3000):
            logger.info("Searching on iteration {}/3000: {}@{}".format(i,subreddit_name, last_post))
            try:
                data, last_post = getPushshiftData(last_post, subreddit_name)
                collected_data = collected_data.append(data, ignore_index=True)
            except Exception as e:
                logger.error(e)
            finally:
                if((int(time.time()) - int(last_post)) >= days_ago*86400 ): # time difference is more than a certain span of seconds (86400 secs in a day)
                    # Break out by throwing a 'Done' error
                    raise Exception("Done")
    except KeyboardInterrupt as e:
        print("Ending search through the {} subreddit".format(subreddit_name))
    except Exception as e:
        print(e)
    return collected_data
    
def reddit():
    """ 
        Steps to pull data from reddit
    """

    subreddits_to_explore = json.load(open("{}/src/data/config/reddit_config.json".format(project_dir)))

    for this_subreddit in subreddits_to_explore["subreddits"]:
        try:
            logger.info("Attempting to fetch data from r/{}".format(this_subreddit["sub_name"]))

            # Using the reddit_config file determine how many days we want to pull from this sub
            try: 
                days_to_pull = this_subreddit["days"]
            except Exception as e: 
                days_to_pull = subreddits_to_explore["default_days"]
                
            subreddit_pull = pull_subreddit_data(this_subreddit["sub_name"], days_to_pull)

            logger.info("Saving r/{} data to: {}/data/raw/reddit/r_{}.json".format(this_subreddit["sub_name"], project_dir, this_subreddit["sub_name"]))

            subreddit_pull.to_json("{}/data/raw/reddit/r_{}.json".format(project_dir, this_subreddit["sub_name"]), orient="index")

        except Exception as e:
            logger.warning(e)
            logger.error("Unable to pull data from the {} subreddit".format(this_subreddit["sub_name"]))

    return 200
    

if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/reddit_data_logs.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running in {}".format(project_dir))

        status = reddit()

        logger.info(status)

    except Exception as e:
        logger.error(e)


