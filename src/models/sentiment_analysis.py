import os
import logging

from tensorflow import keras
import numpy as np
import pandas as pd
from pathlib import Path

logger = logging.getLogger("SentimentML")
project_dir = "./"



if __name__ == "__main__":
    try:
        project_dir = Path(__file__).resolve().parents[2]
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/src/models/logs/SentimentML.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running model in {}".format(project_dir))

        sentiment_data = pd.read_json("{}/data/interim/reddit_processed.json".format(project_dir))

    except Exception as e:
        logger.error("An Error Occured: {}".format(e))