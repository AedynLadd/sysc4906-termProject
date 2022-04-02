from shutil import ExecError
import numpy as np
import pandas as pd
import json
import logging
from pathlib import Path
from matplotlib import pyplot as plt
from statsmodels.tsa.vector_ar.var_model import VAR

logger = logging.getLogger("VAR")

REGRESSION_DAYS_USED = 135
NUM_OBS = 7
validate_or_predict = "predict"

def create_model(data):
    train = data[:-NUM_OBS]
    model = VAR(train)

    results = model.fit(3)
    # logger.info(results.summary())
    return results

def invert_transformation(df_train, df_forecast, diff_used):
    """Revert back the differencing to get the forecast to original scale."""
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        #df_fc[str(col)+'_2d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2] - df_train[col].iloc[-3]) + df_fc[str(col)+'_3d'].cumsum()
        df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_nd'].cumsum()
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()

    return df_fc

def forecast_model(model, input_data, original_data, diff_used = 2):
    lag_order = model.k_ar

    logger.info("LAG ORDER IS: {} ".format(lag_order))
    
    if validate_or_predict == "validate":
        forecasting_input = input_data.values[-(lag_order + NUM_OBS):-NUM_OBS]
        forecast_intervals = model.forecast_interval(forecasting_input, alpha=0.95, steps=NUM_OBS)

        idx = pd.date_range(str(original_data.index[-NUM_OBS]), periods=NUM_OBS, freq='D')

        forecast_data = pd.DataFrame(forecast_intervals[0], index = idx, columns= input_data.columns + '_nd')
        forecast_intervals_up = pd.DataFrame(forecast_intervals[2], index=idx, columns=input_data.columns + "_nd")
        forecast_intervals_down = pd.DataFrame(forecast_intervals[1], index=idx, columns=input_data.columns + "_nd")
    else:   
        forecasting_input = input_data.values[-lag_order:]
        forecast_intervals = model.forecast_interval(forecasting_input, alpha=0.95, steps=NUM_OBS)

        idx = pd.date_range(str(original_data.index[-1]), periods=NUM_OBS, freq='D')
        
        forecast_data = pd.DataFrame(forecast_intervals[0], index = idx, columns= input_data.columns + '_nd')
        forecast_intervals_up = pd.DataFrame(forecast_intervals[2], index=idx, columns=input_data.columns + "_nd")
        forecast_intervals_down = pd.DataFrame(forecast_intervals[1], index=idx, columns=input_data.columns + "_nd")

    reTransformed_forecast = invert_transformation(original_data, forecast_data, diff_used)
    reTransformed_forecast_interval_up = invert_transformation(original_data, forecast_intervals_up, diff_used)
    reTransformed_forecast_interval_down = invert_transformation(original_data, forecast_intervals_down, diff_used)
    
    return reTransformed_forecast, reTransformed_forecast_interval_up, reTransformed_forecast_interval_down


def format_sentiment_and_coin_data(coin_data, sentiment_data, bitcoin_sentiment):
    coin_data = pd.DataFrame(coin_data)
    coin_specific_sentiment = sentiment_data.apply(pd.Series)[["count","sentiment"]].dropna()
    bitcoin_specific_sentiment = bitcoin_sentiment.apply(pd.Series)[["sentiment"]].dropna()

    bitcoin_specific_sentiment.columns = ['btc_sentiment']

    coin_data["timestamp"] = pd.to_datetime(coin_data["timestamp"]).dt.date

    coin_specific_sentiment.reset_index(inplace=True)
    coin_specific_sentiment.rename(columns = {"index": 'timestamp'}, inplace=True)
    coin_specific_sentiment["timestamp"] = pd.to_datetime(coin_specific_sentiment["timestamp"]).dt.date

    bitcoin_specific_sentiment.reset_index(inplace=True)
    bitcoin_specific_sentiment.rename(columns = {"index": 'timestamp'}, inplace=True)
    bitcoin_specific_sentiment["timestamp"] = pd.to_datetime(coin_specific_sentiment["timestamp"]).dt.date

    specific_sentiment = pd.merge(left = coin_specific_sentiment, right=bitcoin_specific_sentiment, how='left', left_on='timestamp', right_on='timestamp')

    merged_data = pd.merge(left=coin_data, right=specific_sentiment, how='left', left_on='timestamp', right_on='timestamp')
    merged_data["sentiment"].fillna(method="bfill", inplace=True)
    merged_data["btc_sentiment"].fillna(method="bfill", inplace=True)
    merged_data["count"].fillna(method="bfill", inplace=True)

    merged_data.index = pd.DatetimeIndex(merged_data["timestamp"]).to_period("d")
    merged_data.drop(labels = "timestamp", axis = 1, inplace=True)
    #  "btc_sentiment"
    merged_data.drop(labels = ["high", "low", "close", "volume", "marketCap", "count", "btc_sentiment"], axis=1, inplace=True)

    merged_data.dropna()

    return merged_data

def vectorAutoRegression(regression_days = REGRESSION_DAYS_USED, observations_made = NUM_OBS):

    REGRESSION_DAYS_USED = regression_days
    NUM_OBS = observations_made

    
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

        coin_forecasting = {}
        forecast_metrics = {}

        for coin_name in coin_data:
            logger.info("Running a Vector AutoRegression on {}".format(coin_name))
            try:
                try:
                    coin_keyword_sentiment_data = keyword_sentiment_data[new_coin_map[str(coin_name)]["symbol"]]
                    bitcoin_sentiment_comparison = keyword_sentiment_data["BTC"]
                except Exception as e:
                    raise(Exception("Sentiment Data does not exist for this coin"))

                merged_data = format_sentiment_and_coin_data(coin_data[coin_name], coin_keyword_sentiment_data, bitcoin_sentiment_comparison)

                df_difference = merged_data.diff().diff().dropna()

                df_difference = df_difference[-REGRESSION_DAYS_USED:]

                model = create_model(df_difference)

                forecast_data, forecast_intervals_up, forecast_intervals_down = forecast_model(model, df_difference, merged_data[-REGRESSION_DAYS_USED:])

                actual_data = merged_data["open"]

                forecast_data = forecast_data["open_forecast"]
                forecast_up_interval = forecast_intervals_up["open_forecast"]
                forecast_down_interval = forecast_intervals_down["open_forecast"]

                saved_actual_data = actual_data[-30:].reset_index()
                saved_actual_data.columns = ["historical_timestamp", "historical_open"]

                saved_actual_timestamps = np.array(saved_actual_data["historical_timestamp"].dt.to_timestamp())
                saved_actual_open = np.array(saved_actual_data["historical_open"])

                if validate_or_predict == "validate":
                    # VALIDATING AGAINST THE PAST
                    forecast_data = forecast_data + (actual_data[-NUM_OBS] - forecast_data[0])
                    forecast_up_interval = forecast_up_interval + (actual_data[-NUM_OBS] - forecast_up_interval[0])
                    forecast_down_interval = forecast_down_interval + (actual_data[-NUM_OBS] - forecast_down_interval[0])

                    # Modify columns
                    mod_data = forecast_data.reset_index()
                    mod_data.columns = ["timestamp", "open_forecast"]
                    
                    mod_up_data = forecast_up_interval.reset_index()
                    mod_up_data.columns = ["timestamp", "upInterval_forecast"]

                    mod_down_data = forecast_down_interval.reset_index()
                    mod_down_data.columns = ["timestamp", "downInterval_forecast"]

                    # Save data in numpy array
                    open_forecast_data = np.nan_to_num(np.array(mod_data["open_forecast"]))
                    forecast_timestamps = np.nan_to_num(np.array(mod_data["timestamp"]))

                    open_up_interval = np.nan_to_num(np.array(mod_up_data["upInterval_forecast"]))
                    open_down_interval = np.nan_to_num(np.array(mod_down_data["downInterval_forecast"]))

                    coin_forecasting[str(coin_name).replace(" ", "_")] = {
                        "forecast":{
                            "timestamp": forecast_timestamps.tolist(),
                            "open_forecast": open_forecast_data.tolist(),
                            "open_up_interval": open_up_interval.tolist(),
                            "open_down_interval": open_down_interval.tolist(),
                        },
                        "past_data":{
                            "timestamp": saved_actual_timestamps.tolist(),
                            "data":saved_actual_open.tolist(),
                        }
                    }
                    
                    actual_compare_data = actual_data[-NUM_OBS:] 
                    
                    residual_forecast_error = np.array(actual_compare_data) - np.array(forecast_data) / np.array(forecast_data)
                    forecast_bias = sum(residual_forecast_error) * 1/len(residual_forecast_error)
                    mean_absolute_error = np.mean(abs(residual_forecast_error))

                    forecast_metrics[str(coin_name).replace(" ", "_")] = {
                        "residual_forecast_error": residual_forecast_error.tolist(),
                        "forecast_bias": forecast_bias.tolist(),
                        "mean_absolute_error": mean_absolute_error.tolist(),
                        "first_error": residual_forecast_error.tolist()[1]
                    }


                else:
                
                    # PREDICTING THE FUTURE
                    forecast_data = forecast_data + (actual_data[-1] - forecast_data[0])
                    forecast_up_interval = forecast_up_interval + (actual_data[-1] - forecast_up_interval[0])
                    forecast_down_interval = forecast_down_interval + (actual_data[-1] - forecast_down_interval[0])
                    
                    # Modifying the columns
                    mod_data = forecast_data.reset_index()
                    mod_data.columns = ["timestamp", "open_forecast"]

                    mod_up_data = forecast_up_interval.reset_index()
                    mod_up_data.columns = ["timestamp", "upInterval_forecast"]

                    mod_down_data = forecast_down_interval.reset_index()
                    mod_down_data.columns = ["timestamp", "downInterval_forecast"]

                    # Storing data in numpy array
                    open_forecast_data = np.nan_to_num(np.array(mod_data["open_forecast"]))
                    forecast_timestamps = np.nan_to_num(np.array(mod_data["timestamp"]))

                    open_up_interval = np.nan_to_num(np.array(mod_up_data["upInterval_forecast"]))
                    open_down_interval = np.nan_to_num(np.array(mod_down_data["downInterval_forecast"]))

                    coin_forecasting[str(coin_name).replace(" ", "_")] = {
                        "forecast":{
                            "timestamp": forecast_timestamps.tolist(),
                            "open_forecast": open_forecast_data.tolist(),
                            "open_up_interval": open_up_interval.tolist(),
                            "open_down_interval": open_down_interval.tolist(),
                        },
                        "past_data":{
                            "timestamp":saved_actual_timestamps.tolist(),
                            "data":saved_actual_open.tolist(),
                        }
                    }
                    
                        
                if coin_name == "Bitcoin":
                    plt.figure("output_{}-{}_{}".format(coin_name, REGRESSION_DAYS_USED, NUM_OBS))
                    actual_data[-30:].plot(y="open")

                    forecast_up_interval.plot(y="up_forecast", color="red")
                    forecast_data.plot(y="open_forecast", color="blue")
                    forecast_down_interval.plot(y="down_forecast", color="red")
                    plt.savefig("{}/src/models/forecasts/graphs/output_{}-{}_{}.jpg".format(project_dir, coin_name, REGRESSION_DAYS_USED, NUM_OBS))

            except Exception as e:
                logger.error("An error has occured {}".format(e))

        if validate_or_predict == "predict":
            # save the forecasting data for display 
            try:
                with open("{}/data/processed/7d_forecast.json".format(project_dir), "w") as json_file:
                        json.dump(coin_forecasting, json_file)
                        
            except Exception as e:
                logger.error("Unable to save the forecasted data")
                print(e)
                
    except Exception as e:
        return 400, {}
    return 200, forecast_metrics

def vectorAutoRegression_summary(metrics):
    logger.info("Summarizing our VAR Statistics")
    try:
        metric_df = pd.DataFrame(metrics).transpose()[["forecast_bias", "mean_absolute_error", "first_error"]]
        
        mean = metric_df.mean()
        return 200, mean
    except Exception as e:
        return 400

if __name__ == "__main__":
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/reddit_data_logs.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])
        
        
        if validate_or_predict == "predict":
            status, metrics = vectorAutoRegression()
            logger.info("VECTOR AUTO REGRESSION HAS COMPLETED - STATUS CODE - {}".format(status))

        else:       
            logger.info("Maximizing validation")
            validation_stats = pd.DataFrame(columns=["trial", "mean_MAE", "mean_forecast_bias"])
            #for days_used in range(12, 12):
            for regressed_days in range(30, 365, 3):   
                try:
                    logger.info("Using {} regression days".format(135))
                    status, metrics = vectorAutoRegression(regressed_days, 7)
                    logger.info("VECTOR AUTO REGRESSION HAS COMPLETED - STATUS CODE - {}".format(status))
                    if(status == 200):
                        status, mean = vectorAutoRegression_summary(metrics)
                        if(status == 200):
                            validation_stats = validation_stats.append({
                                "trial": "{}-{}".format(regressed_days, 7),
                                "mean_forecast_bias": mean["forecast_bias"], 
                                "mean_MAE": mean["mean_absolute_error"],
                                "first_forecast_error": metrics["first_error"]
                            }, ignore_index=True)

                except Exception as e:
                    logger.info("error computing {}".format(e))

            validation_stats.to_json("{}/src/models/forecasts/optimization.json".format(project_dir), orient="index")

            min_validation = validation_stats.min()
            logger.info("OPTIMAL VALUE IS {}".format(min_validation))
    except Exception as e:
        logger.error("An Error has occured {}".format(e))