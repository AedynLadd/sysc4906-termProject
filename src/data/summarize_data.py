
import os
import sys
import time
import json
import logging
import datetime
import numpy
import pandas as pd
from pathlib import Path

logger = logging.getLogger("SummarizeData")
project_dir = "./"

def boolean_df(item_lists, unique_items):
    # Create empty dict
    bool_dict = {}
    
    # Loop through all the tags
    for i, item in enumerate(unique_items):
        # Apply boolean mask
        bool_dict[item] = item_lists.apply(lambda x: 1 if item in x else 0)
            
    # Return the results as a dataframe
    return pd.DataFrame(bool_dict)

def sub_df_analysis(x):
    try:
        number_posts = x["data"].count()

        sentiment_df = pd.DataFrame()
        sentiment_df["positive_sentiment"] = (x["sentiment"].map(lambda v: v["pos"]) * x["score"])
        sentiment_df["negative_sentiment"] = (x["sentiment"].map(lambda v: v["neg"]) * x["score"])
        sentiment_df["neutral_sentiment"]  = (x["sentiment"].map(lambda v: v["neu"]) * x["score"])

        unique_keywords = [keyword for keyword in x["keywords"].explode(ignore_index=True).unique() if not pd.isnull(keyword)]

        boolean_mask = boolean_df(x["keywords"], unique_keywords)

        if boolean_mask.empty:
            return pd.Series({
                "number_of_posts": number_posts,
                "overall_positivity_sum": sentiment_df["positive_sentiment"].sum(),
                "overall_negativity_sum": sentiment_df["negative_sentiment"].sum(),
                "overall_neutrality_sum": sentiment_df["neutral_sentiment"].sum(),
                "keyword_based_sentiment": {}
                })
        else:
            keyword_post_count_mask = boolean_mask.sum()
            keyword_sentiment_mask = (boolean_mask.multiply(sentiment_df["positive_sentiment"], axis="index") + (-1*boolean_mask.multiply(sentiment_df["negative_sentiment"], axis="index"))).sum()
            
            test = pd.concat([keyword_post_count_mask.rename("count"), keyword_sentiment_mask.rename("sentiment")], axis=1, join="inner").transpose()
            
            return pd.Series({
                "number_of_posts": number_posts,
                "overall_positivity_sum": sentiment_df["positive_sentiment"].sum(),
                "overall_negativity_sum": sentiment_df["negative_sentiment"].sum(),
                "overall_neutrality_sum": sentiment_df["neutral_sentiment"].sum(),
                "keyword_based_sentiment": test.to_dict()
                })
    except Exception as e:
        print(x)
        logger.error("An error occured {}".format(e))
            


def summarize_data(data_file):

    summarized_data = data_file.groupby(["timestamp"]).apply(sub_df_analysis)
    
    return summarized_data

if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/summarize_data.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running in {}".format(project_dir))

        reddit_corpus = pd.read_json("{}/data/interim/reddit_processed.json".format(project_dir))
        summary = summarize_data(reddit_corpus)

        summary.to_json("{}/data/processed/{}_summary.json".format(project_dir, "reddit"), orient="index")
        logger.info("Data Summary Completed")
    except Exception as e:
        logger.error(e)
