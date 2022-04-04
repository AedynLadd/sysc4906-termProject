import json
import numpy as np
import pandas as pd
from pathlib import Path
import logging
from matplotlib import pyplot as plt
from scipy import signal
from scipy import stats
import statsmodels.tsa.stattools as ts 
from statsmodels.tsa.vector_ar.vecm import coint_johansen


logger = logging.getLogger("X-correlation")

def invert_transformation(df_train, df_forecast, diff_used):
    """Revert back the differencing to get the forecast to original scale."""
    df_fc = df_forecast.copy()
    columns = df_train.columns

    for col in columns:        
        df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_nd'].cumsum()
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()

    return df_fc


def format_sentiment_and_coin_data(coin_data, sentiment_data):
    # Start by formatting our coin data
    coin_data = pd.DataFrame(coin_data)
    coin_specific_sentiment = sentiment_data.apply(pd.Series)[["count","sentiment"]].dropna()

    # extract the timestamps and turn them into proper date time format
    coin_data["timestamp"] = pd.to_datetime(coin_data["timestamp"]).dt.date

    # remove the indices from our sentiment data
    coin_specific_sentiment.reset_index(inplace=True)
    coin_specific_sentiment.rename(columns = {"index": 'timestamp'}, inplace=True)
    # extract timestamps same as before
    coin_specific_sentiment["timestamp"] = pd.to_datetime(coin_specific_sentiment["timestamp"]).dt.date

    # merge our coin sentiment and money data on the timestamp column
    merged_data = pd.merge(left=coin_data, right=coin_specific_sentiment, how='left', left_on='timestamp', right_on='timestamp')
    
    # Our method of imputation for this will simply be a backfill - A gradual decrease to 0 would be better for sentiment however
    # for the sake of this study normal backfill is fine
    merged_data["sentiment"].fillna(method="ffill", inplace=True)
    merged_data["count"].fillna(method="ffill", inplace=True)

    # turn timestamp column into our new indexing
    merged_data.index = pd.DatetimeIndex(merged_data["timestamp"]).to_period("d")
    merged_data.dropna()
    merged_data["sentiment_log"] = np.log10(abs(merged_data['sentiment']) + 0.00001)
    merged_data['z_score'] = stats.zscore(merged_data['sentiment_log'], nan_policy="omit")

    merged_data = merged_data.loc[merged_data['z_score'].abs()<= 3 ]
    merged_data.drop(labels = "timestamp", axis = 1, inplace=True)
    merged_data.drop(labels = ["high", "low", "close", "volume", "marketCap", "count", "z_score", "sentiment_log"], axis=1, inplace=True)

    # any  still existing NAs can be dropped (but should have been backfilled several steps ago)
    merged_data.dropna()

    return merged_data

def compute_cointegration_EG_(original_data, alpha=0.05):
    result=ts.coint(original_data["open"], original_data["sentiment"])
    return 1 if result[1] > alpha else 0

def compute_cointegation_J_(original_data, alpha = 0.05):
    """Perform Johanson's Cointegration Test and Report Summary"""
    out = coint_johansen(original_data,1,2)
    d = {'0.90':0, '0.95':1, '0.99':2}
    traces = out.lr1
    cvts = out.cvt[:, d[str(1-alpha)]]

    # Summary
    results = []
    for col, trace, cvt in zip(original_data.columns, traces, cvts):
        results.append(1 if trace > cvt else 0)
    return sum(results)


def compute_cross_correlation(dataset1, dataset2):
    lags = np.arange(-(100), (100), 1)  # uncontrained
    rs = np.nan_to_num([dataset1.copy().corr(dataset2.copy().shift(lag)) for lag in lags])

    return lags[np.argmax(rs)], np.max(rs)

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt,
                        handlers= [
                            logging.FileHandler("{}/logs/reddit_data_logs.log".format(project_dir), mode = "w"),
                            logging.StreamHandler()
                        ])
        
    try:
        coin_mapping_file = open("{}/data/raw/coinmarketcap/top_100_coins.json".format(project_dir))
        coin_mapping = json.load(coin_mapping_file)["coins"]

        new_coin_map = {}
        for coin_features in coin_mapping: 
            new_coin_map[coin_features["name"]] = coin_features
        coin_file = open("{}/data/raw/coinmarketcap/historical_data.json".format(project_dir))
        coin_data = json.load(coin_file)

        sentiment_data_df = pd.read_json("{}/data/processed/reddit_summary_all.json".format(project_dir), orient="index")
        keyword_sentiment_data = sentiment_data_df["keyword_based_sentiment"].apply(pd.Series)
        
        x_correlation_stats = {}
        counter = 0
        for coin_name in coin_data:
            logger.info("Running a cross correlation on sentiment v. open price for {}".format(coin_name))
            try:
                try:
                    coin_keyword_sentiment_data = keyword_sentiment_data[new_coin_map[str(coin_name)]["symbol"]]
                except Exception as e:
                    raise(Exception("Sentiment Data does not exist for this coin"))
                
                merged_data = format_sentiment_and_coin_data(coin_data[coin_name], coin_keyword_sentiment_data)
                
                if(len(merged_data) <= 20):
                    raise Exception("Not Enough Data Present")
                else:
                    counter += 1
                    if coin_name == "Bitcoin":
                        plt.figure('Comparison of Open and Sentiment of {}'.format(coin_name))
                        figs, ax = plt.subplots(2,1,figsize=(10,6), sharex=True)
                        
                        ax[0].plot(np.array(merged_data["open"]), color="b", label="Opening Cost")
                        ax[0].legend()

                        ax[1].plot(np.array(merged_data["sentiment"]), color="r", label="Sentiment Value")
                        ax[1].legend()
                        plt.savefig("{}/src/models/x-correlation/output_time_series_{}.jpg".format(project_dir, coin_name))
                        plt.close('all')

                    # Previous analysis indicates that original data is stationary - Must take the second difference before continuing analysis
                    df_difference = merged_data.diff().diff().dropna()

                    if coin_name == "Bitcoin":
                        plt.figure('Comparison of Second Difference - Open and Sentiment of {}'.format(coin_name))
                        figs, ax = plt.subplots(2,1,figsize=(10,6), sharex=True)
                        
                        ax[0].plot(np.array(df_difference["open"]), color="b", label="Opening Cost")
                        ax[0].legend()

                        ax[1].plot(np.array(df_difference["sentiment"]), color="r", label="Sentiment Value")
                        ax[1].legend()
                        plt.savefig("{}/src/models/x-correlation/output_time_series_2ndDifference_{}.jpg".format(project_dir, coin_name))
                        plt.close('all')

                    lags, xcorr = compute_cross_correlation(df_difference["open"], df_difference["sentiment"])

                    #Engle Granger test
                    coint_test_J = compute_cointegation_J_(merged_data)
                    coint_test_EG = compute_cointegration_EG_(merged_data)
                    x_correlation_stats[coin_name] = {
                        "lag": abs(float(lags)),
                        "xcorr": float(xcorr),
                        "Jcoint": coint_test_J,
                        "EGcoint": coint_test_EG,
                    }
               
            except Exception as e:
                logger.info("An error has occured for this coin -> {}".format(e))

        df_x_corr = pd.DataFrame.from_dict(x_correlation_stats).transpose()

        x_correlation_stats["_average"] = {
            "lag": df_x_corr["lag"].mean(),
            "xcorr": df_x_corr["xcorr"].mean(),
            "Jcoint": df_x_corr["Jcoint"].mean()/2,
            "EGcoint": df_x_corr["EGcoint"].mean()
        }

        with open("{}/src/models/x-correlation/correlation_stats.json".format(project_dir), "w") as json_file:
            json.dump(x_correlation_stats, json_file)
        
    except Exception as e:
        logger.error("An error has occured running the script!")
