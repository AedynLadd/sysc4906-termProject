
import re
import json
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger("TextProcessing")
project_dir = "./"

text_process_config = json.load(open("{}/src/data/config/text_process_config.json".format(project_dir)))

def tokenize(input_text):
    """
        We begin with tokenization - we split our text into just words
        all words will be lowercase and punctuation will be removed
    """
    reg_expressions = [r'http\S+',  # Remove any hyperlinks
                       r'[\W]+',    # Identify words
                       r'[0-9]+'    # Identify and remove numbers
                      ]
    for reg in reg_expressions:
        input_text = re.sub(reg, " ", input_text)

    return input_text.lower()


def filter_raw(loaded_raw):
    """
        defines all necessary steps to filter our raw data including adding to our bag of words
    """
    tokenized_text = ""

    try:
        tokenized_text = [token for token in tokenize(loaded_raw).split(" ") if len(token) > 1]
        tokenized_text = " ".join(tokenized_text)
    except Exception as e:
        logger.error("An Error Occured Tokenizing : {}".format(e))
    finally:
        return tokenized_text

def validate_key(data, key):
    """
        Validates that a key exists or not
    """
    try:
        return data[key[0]]
    except Exception as e:
        return "NAN"

def process_data(filename):
    """
        Process the data
    """
    logger.info("Processing data in: {}".format(str(filename)))
    processed_data = pd.DataFrame()

    try:
        # Our first step is to load in the data from our raw json file:
        loaded_raw = pd.read_json(filename, orient="index")
        # Our next step is to filter our raw data - This will include both the selftext and the title
        loaded_raw["combined_text_data"] = loaded_raw["title"] + loaded_raw["selftext"]
        # Apply our text filter to this new column
        processed_data["source"] = validate_key(loaded_raw, ["subreddit"])
        processed_data["timestamp"] = validate_key(loaded_raw, ["created_utc"])
        processed_data["data"] = validate_key(loaded_raw, ["combined_text_data"]).apply(filter_raw)
        processed_data["score"] = validate_key(loaded_raw, ["score"])

    except Exception as e:
        logger.info("An Error Occured when processing at the filepath {}: {}".format(filename, e))

    finally:
        return processed_data

if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/text_process.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running in {}".format(project_dir))

        for data_source_name in text_process_config["data_stores"]:
            logger.info("Running through {} data".format(data_source_name))
            try:
                data_source_path = "{}/data/raw/{}".format(project_dir, data_source_name)
                
                analyzed_data = pd.concat([process_data(filename) for filename in Path(data_source_path).glob('*') if (not ("gitkeep" in str(filename)))])
                analyzed_data = analyzed_data.sort_values(by="timestamp", ascending=True, ignore_index=True)
                # Save data to a json
                analyzed_data.to_json("{}/data/interim/{}_processed.json".format(project_dir, data_source_name), orient="records")

            except Exception as e:
                logger.error("Error Occured when processing {} data: {}".format(data_source_name, e))

        logger.info("Text Analysis Completed")
    except Exception as e:
        logger.error(e)

