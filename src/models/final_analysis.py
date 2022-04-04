import numpy as np
import matplotlib.pyplot as plt
import json
import logging
import datetime
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import os
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts

"""
    final_analysis.py contains the final phase code for the correlation analysis between
    coin prices and sentiment values. 
    
    Running the program will read the CoinMarketCap coin price data found in 
    data/raw/coin market cap and Reddit sentiment values found under
    data/processed/reddit_summary_all.json
    
    This data will then be converted to stationary data via taking the differences and
    then a variety of methods will be used on that stationary data to quantify the
    amount of correlation between coin prices and sentiment
"""

logger = logging.getLogger('final_analysis')
project_dir = '../src/data/'

force_lag_days_offset = 0

# keep both of these as False to quickly go through
# all 100 coins and get an overall summary at the end
show_plots = False
save_figure_pngs = False


"""
    Calculates the population covariance for values x and y
"""
def population_covariance(x, y):
    mean_x = sum(x) / float(len(x))
    mean_y = sum(y) / float(len(y))
    sub_x = [i - mean_x for i in x]
    sub_y = [i - mean_y for i in y]
    numerator = sum([sub_x[i] * sub_y[i] for i in range(len(sub_x))])
    denominator = len(x)
    cov = numerator / denominator
    return cov


"""
    Takes in some data and computes the differences of that data
    and then returns the differences
"""
def compute_diffs(data):
    diffs_with_dates = {}
    just_diffs = []
    for date in data:
        # fetch next day key for dictionary
        temp = list(data)
        try:
            next_date = temp[temp.index(date) + 1]
        except (ValueError, IndexError):
            next_date = None

        if next_date is not None and data[date] != 0:
            # compute difference between current value and next day's val
            difference = data[next_date] - data[date]

            # print('-----------------------------------------------------------------')
            # print('current day is ', date, ' with a value of ', coin_prices[date])
            # print('The next day is : ' + str(next_date), ' with a value of ', coin_prices[next_date])

            # append diff to dictionary
            diffs_with_dates[date] = difference
            just_diffs.append(difference)

    return diffs_with_dates, just_diffs



"""
    Uses ADF test to check whether data is stationary, if not
    stationary it will continually differentiate the data until
    is passes the ADF test and is stationary
    
    https://www.youtube.com/watch?v=bP1fbXd_XSk
    https://www.statology.org/dickey-fuller-test-python/
"""
def make_data_stationary(data):
    diffs_taken = 0

    adf = adfuller(list(data.values()))
    p_val = adf[1]
    print("initial ADF test before hand:")

    if p_val >= 0.05:
        print("data is non-stationary and will be converted to stationary")
        diff_with_dates, just_diffs = compute_diffs(data)
        diffs_taken += 1

        # perform augmented Dickey-Fuller test (ADF)
        adf = adfuller(just_diffs)
        p_val = adf[1]

        num_iterations = 1
        if p_val >= 0.05:
            while p_val >= 0.05:
                diff_with_dates, just_diffs = compute_diffs(diff_with_dates)
                diffs_taken += 1
                adf = adfuller(just_diffs)
                p_val = adf[1]
                num_iterations += 1

        print(num_iterations, "differences were taken to make data stationary")

        # return the new stationary data
        return diff_with_dates, diffs_taken
    else:
        print("data was stationary to begin with")
        # just return data without changes
        return data, 0


"""
    cointegration test taken from
    https://stackoverflow.com/questions/11362943/efficient-cointegration-test-in-python
"""
def cointegration_test(y, x):
    # Step 1: regress on variable on the other
    ols_result = sm.OLS(y, x).fit()
    # Step 2: obtain the residual (ols_resuld.resid)
    # Step 3: apply Augmented Dickey-Fuller test to see whether
    #        the residual is unit root
    return ts.adfuller(ols_result.resid)

"""
    main function that performs the full analysis
    on all 100 coins
"""
def perform_analysis():
    sum_of_pearson_corr_coeffs = 0
    sum_of_cross_corrs = 0
    sum_of_cross_corr_index = 0
    sum_of_covariances = 0

    sum_of_coin_diffs_taken = 0
    num_coin_diffs_taken = 0
    sum_of_sentiment_diffs_taken = 0
    num_sentiment_diffs_taken = 0

    sum_of_coin_dw_vals = 0
    num_coin_dw_vals = 0
    sum_of_sentiment_dw_vals = 0
    num_sentiment_dw_vals = 0

    num_cointegration_present = 0
    num_coint_results = 0

    num_coins_looked_at = 0

    # first convert reddit_summary_all.json to a python dictionary
    with open(str(project_dir) + '/data/processed/reddit_summary_all.json') as json_file:
        reddit_sentiment_data = json.load(json_file)

    # for each coin file in data/raw/coin market cap
    directory = str(project_dir) + '/data/raw/coin market cap'
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        if os.path.isfile(f) and 'tickers.csv' not in f:

            # Opening JSON file
            with open(f) as json_file:
                coin_data = json.load(json_file)

                coin_name = coin_data['data']['name']
                coin_symbol = coin_data['data']['symbol']

                print("\n===============================================")
                print("                " + coin_name)
                print("===============================================")
                print("coin name:", coin_data['data']['name'])
                print("coin symbol:", coin_data['data']['symbol'])

                # =====================================================
                # Step 1 read coin prices and dates for those prices
                # =====================================================
                print("-------------- coin price data ----------------")
                coin_prices = {}
                for day in coin_data['data']['quotes']:
                    # coin_prices.append(day['quote']['open'])
                    date = datetime.strptime(day['timeOpen'][0:10], '%Y-%m-%d')
                    coin_prices.update({date: day['quote']['open']})
                print("coin price data:")
                print(coin_prices)
                print(len(coin_prices), ' coin price data points')

                # converting coin price data to stationary data
                coin_differences, num_diffs = make_data_stationary(coin_prices)
                sum_of_coin_diffs_taken += num_diffs
                num_coin_diffs_taken += 1

                # Durbin watson test
                # https://www.geeksforgeeks.org/statsmodels-durbin_watson-in-python/
                dw = durbin_watson(list(coin_differences.values()))
                print("Durbin watson test", dw)
                sum_of_coin_dw_vals += dw
                num_coin_dw_vals += 1

                # =====================================================
                #  Step 2 sentiment values and dates for those prices
                # =====================================================
                print("-------------- sentiment data -----------------")
                sentiment_values = {}
                for timestamp in reddit_sentiment_data:
                    day_data = reddit_sentiment_data[timestamp]
                    # print(day_data["keyword_based_sentiment"])

                    for symbol in day_data["keyword_based_sentiment"]:
                        if symbol == coin_symbol:
                            # print(day_data["keyword_based_sentiment"][symbol])
                            date = datetime.fromtimestamp(int(timestamp[:len(timestamp) - 3])).replace(hour=0)

                            # shift the date to account for lag
                            date = date - timedelta(days=force_lag_days_offset)

                            sentiment_values.update({date: day_data["keyword_based_sentiment"][symbol]['sentiment']})

                print("sentiment data:")
                print(sentiment_values)
                print(len(sentiment_values), ' sentiment data points')


                if sentiment_values: #  if dict is not empty

                    # converting sentiment data to stationary data
                    sentiment_differences, num_diffs = make_data_stationary(sentiment_values)
                    sum_of_sentiment_diffs_taken += num_diffs
                    num_sentiment_diffs_taken += 1

                    # Durbin watson test
                    # https://www.geeksforgeeks.org/statsmodels-durbin_watson-in-python/
                    dw = durbin_watson(list(sentiment_differences.values()))
                    print("Durbin watson test", dw)
                    sum_of_sentiment_dw_vals += dw
                    num_sentiment_dw_vals += 1

                    # ================================================================================
                    #  Step 3 check where the coin price diffs and sentiment diffs share common dates
                    # ================================================================================
                    num_matches = 0
                    matching_coin_diffs = []
                    matching_sentiment_diffs = []
                    for date in coin_differences:
                        if date in sentiment_differences:
                            num_matches += 1
                            matching_coin_diffs.append(coin_differences[date])
                            matching_sentiment_diffs.append(sentiment_differences[date])
                    print(num_matches, ' data points with common dates were found')

                    # also check for common dates for the non-differentiated prices and sentiment values
                    matching_coin_prices = []
                    matching_sentiment_values = []
                    for date in coin_prices:
                        if date in sentiment_values:
                            matching_coin_prices.append(coin_prices[date])
                            matching_sentiment_values.append(sentiment_values[date])

                    # plot non-differentiated prices vs sentiment values
                    # --------------------------------------------------------
                    # clear any previous plots
                    plt.clf()

                    title = coin_name + " Price vs Sentiment"
                    plt.scatter(matching_sentiment_values, matching_coin_prices)
                    plt.title(title)
                    plt.xlabel('Reddit Sentiment Score')
                    plt.ylabel('Coin Price ($)')

                    # save figure under reports/figures
                    if save_figure_pngs:
                        plt.savefig('{}/reports/figures/phase3/{}/{}'.format(project_dir, coin_name, (title + '.png')))

                    # show plot
                    if show_plots:
                        plt.show()

                    # also plot price diffs vs sentiment diffs
                    # -----------------------------------------------

                    # clear any previous plots
                    plt.clf()

                    title = coin_name + " Price difference(s) vs Sentiment difference(s)"
                    plt.scatter(matching_sentiment_diffs, matching_coin_diffs)
                    plt.title(title)
                    plt.xlabel('Reddit Sentiment Score difference(s)')
                    plt.ylabel('Coin Price difference(s) ($)')

                    # save figure under reports/figures
                    if save_figure_pngs:
                        plt.savefig('{}/reports/figures/phase3/{}/{}'.format(project_dir, coin_name, (title + '.png')))

                    # show plot
                    if show_plots:
                        plt.show()

                    # ===========================================
                    # step 4 data analysis portion
                    # ===========================================
                    print("------------------ analysis -------------------")
                    if len(matching_coin_diffs) != 0:  # some coins had no matches
                        num_coins_looked_at += 1

                        # Pearson's correlation analysis
                        # usually you don't want to perform Pearson's on timeseries data however according to this:
                        # https://stats.stackexchange.com/questions/133155/how-to-use-pearson-correlation-correctly-with-time-series
                        # (scroll down to third answer)
                        # you can still find the Pearson's for the differentiated data
                        # ----------------------------------------------
                        correlation_coeff = np.corrcoef(matching_coin_diffs, matching_sentiment_diffs)
                        print('Pearson correlation_coeff:', correlation_coeff[0][1])
                        sum_of_pearson_corr_coeffs += float(correlation_coeff[0][1])

                        # covariance
                        # ----------------------------------------------
                        cov = population_covariance(matching_coin_diffs, matching_sentiment_diffs)
                        print('covariance:', cov)
                        sum_of_covariances += cov

                        # cross correlation coefficients
                        # ----------------------------------------------
                        a = (matching_coin_diffs - np.mean(matching_coin_diffs)) / (
                                np.std(matching_coin_diffs) * len(matching_coin_diffs))
                        b = (matching_sentiment_diffs - np.mean(matching_sentiment_diffs)) / (
                            np.std(matching_sentiment_diffs))
                        c = np.correlate(a, b, 'full')
                        lst = c.tolist()
                        print("max cross correlation value:", max(lst))

                        # amount of lag days
                        # ----------------------------------------------
                        print("index of max val (amount of lag days):", lst.index(max(lst)))
                        sum_of_cross_corr_index += lst.index(max(lst))
                        sum_of_cross_corrs += max(c)

                        # linear regression
                        # ----------------------------------------------
                        coeff = np.polyfit(matching_sentiment_diffs, matching_coin_diffs, 1)
                        print('linear regression slope:', coeff[0])
                        print('linear regression intercept:', coeff[1])
                        poly1d_fn = np.poly1d(coeff)

                        # clear any previous plots
                        plt.clf()

                        title = coin_name + " Linear Regression of Price difference(s) vs Sentiment difference(s)"
                        plt.scatter(matching_sentiment_diffs, matching_coin_diffs)
                        plt.title(title)
                        plt.xlabel('Reddit sentiment score difference(s)')
                        plt.ylabel('Coin price difference(s)')


                        plt.plot(matching_sentiment_diffs, matching_coin_diffs, 'yo', matching_sentiment_diffs,
                                 poly1d_fn(matching_sentiment_diffs))  # 'yo' = yellow circle marker

                        # save figure under reports/figures
                        if save_figure_pngs:
                            plt.savefig('{}/reports/figures/phase3/{}/{}'.format(project_dir, coin_name, (title + '.png')))

                        # show plot
                        if show_plots:
                            plt.show()

                        # testing cointegration
                        # https://stackoverflow.com/questions/56167373/how-to-read-test-results-if-i-am-using-johansen-test-to-determine-correlation-be
                        # (scroll down to first answer to find the code)
                        # ----------------------------------------------

                        # using original coin prices and sentiment values (not the differenced data)
                        result = ts.coint(matching_coin_prices, matching_sentiment_values)

                        p_val = result[1]
                        if p_val >= 0.05:
                            print("no cointegration")
                        else:
                            print("cointegration is present")
                            num_cointegration_present += 1
                        num_coint_results += 1

    # ==============================
    # step 5 summary statistics
    # ==============================

    print('\n===========================================')
    print('           summary statistics              ')
    print('===========================================')

    # summary of correlation coefficients
    average_corr_coeff = sum_of_pearson_corr_coeffs / num_coins_looked_at
    print('average pearson correlation coefficient:', round(average_corr_coeff, 6))

    # summary of covariances
    average_cov = sum_of_covariances / num_coins_looked_at
    print('average covariance:', round(average_cov, 6))

    # summary of cross correlation coefficients
    average_cross_corr = sum_of_cross_corrs / num_coins_looked_at
    print('average cross correlation coefficient:', round(average_cross_corr, 6))

    # summary of cross correlation index
    average_cross_corr_index = sum_of_cross_corr_index / num_coins_looked_at
    print('average amount of lag days:', round(average_cross_corr_index, 6))

    # number of differences taken to make data stationary
    average_coin_diffs_taken = sum_of_coin_diffs_taken / num_coin_diffs_taken
    print('average coin diffs taken to make data stationary:', round(average_coin_diffs_taken, 6))
    average_sentiment_diffs_taken = sum_of_sentiment_diffs_taken / num_sentiment_diffs_taken
    print('average sentiment diffs taken to make data stationary:', round(average_sentiment_diffs_taken, 6))

    # Durbin Watson values
    average_coin_dw = sum_of_coin_dw_vals / num_coin_dw_vals
    print('average coin Durbin watson value (after data was converted to stationary):', round(average_coin_dw, 6))
    average_sentiment_dw = sum_of_sentiment_dw_vals / num_sentiment_dw_vals
    print('average sentiment Durbin watson value (after data was converted to stationary):', round(average_sentiment_dw, 6))

    # cointegration results
    percent_of_coins_where_cointegration_is_present = (num_cointegration_present / num_coint_results) * 100
    print(round(percent_of_coins_where_cointegration_is_present, 6), "% of coins have cointegration")

"""
    main function just runs the perform_analysis function
"""
if __name__ == '__main__':
    try:

        logger.info('Done')

        project_dir = Path(__file__).resolve().parents[1]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers=[
                                logging.FileHandler('{}/logs/final_analysis.log'.format(project_dir), mode='w'),
                                logging.StreamHandler()
                            ])

        logger.info('performing analysis')
        perform_analysis()

    except Exception as e:
        logger.error('An Error Occured: {}'.format(e))