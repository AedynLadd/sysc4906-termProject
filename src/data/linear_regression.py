import numpy as np
import matplotlib.pyplot as plt
import json
import logging
import datetime
from datetime import datetime
from pathlib import Path
from dateutil import rrule
import os


# # CALCULATING LAG
# # https://stackoverflow.com/questions/49372282/find-the-best-lag-from-the-numpy-correlate-output
# data_1 = np.sin(np.linspace(0, 10, 100))
# data_1 += np.random.uniform(size=data_1.shape)   # noise
# data_2 = np.cos(np.linspace(0, 7, 70))
# data_2 += np.random.uniform(size=data_2.shape)   # noise
#
# corr = np.correlate(data_1 - np.mean(data_1),
#                     data_2 - np.mean(data_2),
#                     mode='full')
# plt.plot(corr)
# plt.show()
# lag = corr.argmax() - (len(data_1) - 1)
# print("lag: ", lag)
# plt.plot(data_1, 'r*')
# plt.plot(data_2, 'b*')
# plt.show()





# # CORRELATION COEFFICIENT AND LINEAR REGRESSION WITH NUMPY POLYFIT FUNCTION
# # https://stackoverflow.com/questions/6148207/linear-regression-with-matplotlib-numpy
# x = [1,2,3,4]
# y = [4,5,7,10]
#
# # correlation coefficient
# correlation_coeff = np.corrcoef(y, x)
# print('correlation_coeff ', correlation_coeff[0][1])
#
# # linear regression
# coef = np.polyfit(x,y,1)
# print('slope ', coef[0])
# print('intercept ', coef[1])
# poly1d_fn = np.poly1d(coef)
# # poly1d_fn is now a function which takes in x and returns an estimate for y
# plt.plot(x,y, 'yo', x, poly1d_fn(x)) #'--k'=black dashed line, 'yo' = yellow circle marker
#
# plt.show()
#



# TESTING homoscedasticity
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bartlett.html



"""
    TODO
"""


logger = logging.getLogger('linear_regression')
project_dir = './'



show_plots = True


"""
    TODO
"""
def linear_regression():
    sum_of_lags = 0
    num_lags = 0
    sum_of_corr_coeffs = 0
    num_corr_coeffs = 0

    # first convert reddit_summary_all.json to a python dictionary
    with open(str(project_dir) + '/data/processed/reddit_summary_all.json') as json_file:
        reddit_sentiment_data = json.load(json_file)
    #print(reddit_sentiment_data)

    # for each coin file in data/raw/coin market cap
    directory = str(project_dir) + '/data/raw/coin market cap'
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        if os.path.isfile(f) and 'tickers.csv' not in f:

            # Opening JSON file
            with open(f) as json_file:
                coin_data = json.load(json_file)

                print("=======================================")
                print("coin name:", coin_data['data']['name'])
                print("coin symbol:", coin_data['data']['symbol'])

                coin_name = coin_data['data']['name']
                coin_symbol = coin_data['data']['symbol']

                # =====================================================
                #  Step 1 read coin prices and dates for those prices
                # =====================================================
                coin_prices = {}
                for day in coin_data['data']['quotes']:
                    # coin_prices.append(day['quote']['open'])
                    date = datetime.strptime(day['timeOpen'][0:10], '%Y-%m-%d')
                    coin_prices.update({date: day['quote']['open']})
                print(coin_prices)
                print(len(coin_prices), ' coin price data points')

                # =====================================================
                #  Step 2 read coin prices and dates for those prices
                # =====================================================
                sentiment_values = {}
                for timestamp in reddit_sentiment_data:
                    day_data = reddit_sentiment_data[timestamp]
                    #print(day_data["keyword_based_sentiment"])

                    for symbol in day_data["keyword_based_sentiment"]:
                        if symbol == coin_symbol:
                            #print(day_data["keyword_based_sentiment"][symbol])
                            date = datetime.fromtimestamp(int(timestamp[:len(timestamp) - 3])).replace(hour=0)
                            sentiment_values.update({date : day_data["keyword_based_sentiment"][symbol]['sentiment']})

                print(sentiment_values)
                print(len(sentiment_values), ' sentiment data points')

                # ===========================================
                #         PRICE vs SENTIMENT
                # ===========================================
                num_matches = 0
                matching_coin_prices = []
                matching_sentiment_vals = []
                for date in coin_prices:
                    if date in sentiment_values:
                        num_matches += 1
                        matching_coin_prices.append(coin_prices[date])
                        matching_sentiment_vals.append(sentiment_values[date])
                print(num_matches, ' data points with common dates were found')

                # show plot
                if show_plots:
                    plt.scatter(matching_sentiment_vals, matching_coin_prices)
                    title = "Price vs Sentiment for " + coin_name
                    plt.title(title)
                    plt.xlabel('Reddit sentiment score')
                    plt.ylabel('Coin Price')
                    plt.show()

                # ===========================================
                #      PRICE CHANGE vs SENTIMENT
                # ===========================================
                coin_percent_changes = {}
                for date in coin_prices:
                    # fetch next day key for dictionary
                    temp = list(coin_prices)
                    try:
                        next_date = temp[temp.index(date) + 1]
                    except (ValueError, IndexError):
                        next_date = None

                    if next_date is not None and coin_prices[date] != 0:
                        # compute percentage change in value by comparing current day value to next day value
                        percent_increase = (coin_prices[next_date] - coin_prices[date]) * 100 / (coin_prices[date])

                        # print('-----------------------------------------------------------------')
                        # print('current day is ', date, ' with a value of ', coin_prices[date])
                        # print('The next day is : ' + str(next_date), ' with a value of ', coin_prices[next_date])
                        # print('percent change is ', round(percent_increase, 5))

                        # append the percentage change to dictionary
                        coin_percent_changes[date] = percent_increase

                num_matches = 0
                matching_coin_prices = []
                matching_sentiment_vals = []
                for date in coin_percent_changes:
                    if date in sentiment_values:
                        num_matches += 1
                        matching_coin_prices.append(coin_percent_changes[date])
                        matching_sentiment_vals.append(sentiment_values[date])
                print(num_matches, ' data points with common dates were found')

                # show plot
                if show_plots:
                    plt.scatter(matching_sentiment_vals, matching_coin_prices)
                    title = "Price Change vs Sentiment for " + coin_name
                    plt.title(title)
                    plt.xlabel('Reddit sentiment score')
                    plt.ylabel('Coin Percentage Price Change')
                    plt.show()

                # ===========================================
                #           data analysis portion
                # ===========================================
                if len(matching_coin_prices) != 0:

                    # ===========================================
                    #           lag analysis
                    # ===========================================

                    corr = np.correlate(matching_coin_prices - np.mean(matching_coin_prices),
                                        matching_sentiment_vals - np.mean(matching_sentiment_vals),
                                        mode='full')
                    # if show_plots:
                    #     plt.plot(corr)
                    #     plt.title("correlation with different lag values")
                    #     plt.show()

                    lag = corr.argmax() - (len(matching_coin_prices) - 1)
                    print("lag value is ", lag)

                    # if show_plots:
                    #     plt.plot(matching_coin_prices, 'r*')
                    #     plt.plot(matching_sentiment_vals, 'b*')
                    #     plt.title("lag")
                    #     plt.show()

                    # used later on in average lag calculations
                    sum_of_lags += lag
                    num_lags += 1

                    # ===========================================
                    #      correlation analysis
                    # ===========================================
                    correlation_coeff = np.corrcoef(matching_coin_prices, matching_sentiment_vals)
                    print('correlation_coeff ', correlation_coeff[0][1])
                    sum_of_corr_coeffs += float(correlation_coeff[0][1])
                    num_corr_coeffs += 1

                    # ===========================================
                    #      linear regression
                    # ===========================================
                    coef = np.polyfit(matching_sentiment_vals,matching_coin_prices,1)
                    print('slope ', coef[0])
                    print('intercept ', coef[1])
                    poly1d_fn = np.poly1d(coef)
                    # poly1d_fn is now a function which takes in x and returns an estimate for y

                    if show_plots:
                        plt.plot(matching_sentiment_vals,matching_coin_prices, 'yo', matching_sentiment_vals, poly1d_fn(matching_sentiment_vals)) #'--k'=black dashed line, 'yo' = yellow circle marker
                        plt.show()

    # ===========================================
    #           summary statistics
    # ===========================================

    print('===========================================')
    print('           summary statistics              ')
    print('===========================================')

    # summary of lags
    average_lag = sum_of_lags / num_lags
    print('average lag value ', average_lag)

    # summary of correlation coefficients
    average_corr_coeff = sum_of_corr_coeffs / num_corr_coeffs
    print('average correlation coefficient ', average_corr_coeff)














"""
    TODO
"""
if __name__ == '__main__':
    try:

        logger.info('Done')

    except Exception as e:
        logger.error('An Error Occured: {}'.format(e))



    #TODO, put back in try catch
    project_dir = Path(__file__).resolve().parents[2]

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt,
                        handlers=[
                            logging.FileHandler('{}/logs/btc_sentiment.log'.format(project_dir), mode='w'),
                            logging.StreamHandler()
                        ])

    logger.info('Computing linear regressions')
    linear_regression()


