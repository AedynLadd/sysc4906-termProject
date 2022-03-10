import json
import time
import logging
import sys
import requests
import pandas as pd
from pathlib import Path

project_dir = "./"
logger = logging.getLogger("CoinMarketCap")

def format_historical_data(historical_data):
    """
        Format the historical data from coinmarketcap to a compressed format thats useful for us
    """

    # Create a place for our historical data to be compiled
    historical_data_slice = {
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": [],
        "marketCap": [],
        "timestamp": []
    }
    
    # Look through the daily quotes
    for quote in historical_data["quotes"]:
        # Cycle through the quotes
        for key, value in {**quote["quote"]}.items():
            # Unpack each quotes key and value
            try:
                historical_data_slice[key].append(value)
            except Exception as e:
                logger.error("An Error has occured trying to load quote data...")
        
    return historical_data_slice

def get_historical_data(coin_id, currencyId, numDays):
    """
        gets the historical data of a specific coin (by the coins id)
        coin_id = bitcoin id as per coinmarketcap.com 
        convertId = Currency id to use
    """
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical"

    params = {
        "id": coin_id,
        "convertId": currencyId,
        "timeStart": int(abs(time.time() - (86400*numDays))), # seconds since epoch (UNIX time)
        "timeEnd": int(time.time())
    }
    
    response = requests.get(url, params)
    
    # Sleep a tiny bit between requests just to make sure we aren't overwellming coinmarketplace
    time.sleep(1)

    return format_historical_data(response.json()["data"])

def get_top_100_coins(upper_limit = 100):
    """
        returns a list of the top 100 coins as described by coinmarketcap.com 
    """

    url = "https://api.coinmarketcap.com/data-api/v3/map/all"

    params = {
        "listing_status": ['active', 'untracked'],
        "exchangeAux": ['is_active','status'],
        "cryptoAux": ['is_active','status'],
        "start": 1, # start at rank 1
        "limit": upper_limit # end at our upper limit which is 100 by default
    }
    # Perform the request
    response = requests.get(url, params)
    
    # Identify the cryptocurrency map from the response
    cryptocurrencyMap = response.json()["data"]["cryptoCurrencyMap"]
    
    x = ""
    for coin in cryptocurrencyMap:
        x += "{}, {}, ".format(coin["slug"],coin["symbol"])
    
    cryptoMapRef = {
        "keyword_metadata": x[0:len(x) - 2],
        "coins": cryptocurrencyMap
    }
    # Save the data for future reference
    with open('{}/data/raw/coinmarketcap/top_100_coins.json'.format(project_dir), 'w') as openfile:
        json.dump(cryptoMapRef, openfile)

    return cryptocurrencyMap

def pull_coinmarketcap_data():
    """
        pull historical data of the top 100 coins listed on the coinmarketcap.com homepage
    """
    try:
        # Get the top 100 crypto currencies
        top_100 = get_top_100_coins()
        
        # Create a blank dictionary where we will store our historical data records
        historical_crypto_data = {}

        index = 0
        for cryptocurrency in top_100:
            index += 1
            logger.info("Compiling Historical Data for {}: {}/100".format(cryptocurrency["name"], index))

            # Try and grab this coins historical data
            try:
                # Save the data into our dictionary
                historical_crypto_data[cryptocurrency["name"]] = get_historical_data(coin_id= cryptocurrency["id"], currencyId = 2784, numDays = 365)
            except Exception as e:
                logger.error("An Error Occured:{}".format(e))
                logger.error("Unable to compile Historical Data for {}".format(cryptocurrency["name"]))

        logger.info("Historical Data has been gathered")

        # Save the historical data to a json file
        with open('{}/data/raw/coinmarketcap/historical_data.json'.format(project_dir), 'w') as openfile:
            json.dump(historical_crypto_data, openfile)

        return 200

    except Exception as e:
        logger.error("An Error Occured: {}".format(e))
        return 400

if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/CoinMarketCap.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        status = pull_coinmarketcap_data()
        logger.info("Done: {}".format(status))

    except Exception as e:
        logger.error("An Error Occured: {}".format(e))
