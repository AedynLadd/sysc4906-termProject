# -*- coding: utf-8 -*-
import os
import requests
import logging
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

    if(res.status_code):
        logger.info("Authentication was a success")
        return res.json()['access_token']
    else:
        raise Exception("Authentication Failed")

def pull_subreddit(subbredit_name, end_date):
    """
        pull all posts from a subbreddit between now and the specified end_date
    """
    
    return None

def main():
    """ 
        Steps to pull data from reddit
    """
    try:
        access_token = authenticate_reddit()
        logger.info("Authentication Token is: {}".format(access_token))
    except Exception as e:
        logger.error(e)
        return 400

    headers = {'User-Agent': 'SYSC_4906/0.0.1', 'Authorization' : 'bearer {}'.format(access_token)}

    authenticate_success = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    project_dir = Path(__file__).resolve().parents[2]

    logger.info("Running in {}".format(project_dir))

    load_dotenv(find_dotenv())
    main()
