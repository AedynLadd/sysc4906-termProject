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
            'subreddit': post['data']['subreddit'],
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

def make_reddit_request(url, params, authentication, subreddit_name, days_ago):
    """
        pull the specificied amount of data using the reddit API
    """
    collected_data = pd.DataFrame()

    try:
        for i in range(1000):
            res = requests.get(url=url, headers= authentication, params=params)

            if(res.status_code == 200):
                    logger.info("Success pulling data from {}".format(subreddit_name))

                    subreddit_slice, last_id, last_post = restructure_subreddit_data(res.json())
            
                    collected_data = collected_data.append(subreddit_slice, ignore_index=True)
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
            time.sleep(2)
    except Exception as e:
        if(e.args[0] == "Done"):
            logger.info("PULL OF DATA FROM r/{} IS DONE".format(subreddit_name))
        else:
            logger.error(e)
            logger.error("Tried searching with response: {}".format(res.json()))

    return collected_data


def pull_subreddit_keyword(subreddit_name, authentication, keywords, days_ago = 1):
    """
        Pull all posts with keywords from a subreddit between now and the specificed amount of days prior
    """
    logger.info("keyword pull being used")
    keyword_query = str(" OR ").join(keywords)

    params = {
        'limit': 100, 
        'restrict_sr': True,
        'q': keyword_query[:512]
    }

    logger.info("searching using params: {}".format(params))
    request_url = "https://oauth.reddit.com/r/{}/search".format(subreddit_name)
    logger.info("MAKING REQUESTS TO: {}".format(request_url))
    logger.info("Searching using the following keywords \n {}".format(keywords))

    subreddit_data = make_reddit_request(url = request_url,
        authentication = authentication,    
        params = params,
        subreddit_name = subreddit_name,
        days_ago = days_ago
        )
    return subreddit_data


def pull_subreddit_data(subreddit_name, authentication, days_ago = 1):
    """
        pull all posts from a subreddit between now and the specified amount of days prior
    """
    logger.info("pulling last 1000 items")
    params = {'limit': 100}
    subreddit_data = pd.DataFrame()
    
    request_url = "https://oauth.reddit.com/r/{}/new".format(subreddit_name)
    logger.info("MAKING REQUESTS TO: {}".format(request_url))

    subreddit_data = make_reddit_request(url = request_url, 
        authentication=authentication,
        params = params,  
        subreddit_name=subreddit_name,
        days_ago=days_ago
        )

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
    authentication_header = {'User-Agent': 'SYSC_4906/1.0.0', 'Authorization' : 'bearer {}'.format(access_token)}
   
    subreddits_to_explore = json.load(open("{}/src/data/config/reddit_config.json".format(project_dir)))

    for this_subreddit in subreddits_to_explore["subreddits"]:
        try:
            logger.info("Attempting to fetch data from r/{}".format(this_subreddit["sub_name"]))

            # Using the reddit_config file determine how many days we want to pull from this sub
            try: 
                days_to_pull = this_subreddit["days"]
            except Exception as e: 
                days_to_pull = subreddits_to_explore["default_days"]

            # Then we determine what kind of pull we are doing!
            try:
                # First check if we want to search using the default keywords
                keywords_to_search = subreddits_to_explore["default_keywords"] if (this_subreddit["keywords"]["use_defaults"]) else []
                keywords_to_search += this_subreddit["keywords"]["extras"] if(len(this_subreddit["keywords"]["extras"]) > 0) else []
                print("keywords to search {}".format(keywords_to_search))
                if(len(keywords_to_search) < 1):
                    raise ValueError("No keywords are listed")

                logger.info("Performing a keyword pull")
                # Now that we have the list of keywords to use, we call the keyword pull function
                subreddit_pull = pull_subreddit_keyword(this_subreddit["sub_name"], 
                    authentication_header, 
                    keywords_to_search, 
                    days_to_pull
                    )

            except KeyError as e:
                print(e)
                logger.info("Performing a Subreddit pull")
                # If no keyword data exists then we pull all data from the subreddit up to x days in the past
                subreddit_pull = pull_subreddit_data(this_subreddit["sub_name"], 
                    authentication_header, 
                    days_to_pull)

            except Exception as e:
                logger.info("An Error Occured: {}".format(e))


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

        # Load in environment variables from .env
        load_dotenv(find_dotenv())

        status = reddit()

        logger.info(status)

    except Exception as e:
        logger.error(e)


