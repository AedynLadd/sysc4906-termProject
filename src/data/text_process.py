
import os
import json
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger("TextProcessing")
project_dir = "./"

def files_to_analyze(project_path):
    """
        Identify files we need to use
    """
    return [filename for filename in Path(project_path).glob('*')]

def load_raw_data():
    return None

def process_text():

    return 200


if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/src/data/logs/text_process.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running in {}".format(project_dir))

        text_process_config = json.load(open("{}/src/data/config/text_process_config.json".format(project_dir)))

        for data_source_name in text_process_config["data_stores"]:
            try:
                data_load = files_to_analyze("{}/data/raw/{}".format(project_dir, data_source_name))

                logger.info(data_load)
            except Exception as e:
                logger.info("Error Occured when processing {} data".format(data_source_name))
        
        logger.info("Text Analysis Completed")
    except Exception as e:
        logger.error(e)

