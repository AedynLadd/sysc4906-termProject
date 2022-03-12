
import json
import logging
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from dateutil import rrule
import os


"""
    btc_sentiment.py looks at the sentiment for all coins on Reddit by
    fetching sentiment scores for all coins overall and then plots the 
    comparison of those values to the actual overall coin prices 
    on CoinMarketCap using matplotlib
"""

logger = logging.getLogger('all_coin_sentiment')
project_dir = './'
save_figure_pngs = True
show_plots = True

# matplotlib font sizes
SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

"""
    Plots the values of dict_to_plot on the y axis and the dates on the x axis
"""
def plot_single_variable(title, dict_to_plot, y_axis_label):
    t1 = [*dict_to_plot]
    data1 = dict_to_plot.values()
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(y_axis_label)

    ax1.plot(t1, data1, color=color)
    ax1.tick_params(axis='y')

    # figure size
    fig.set_size_inches(12, 5)

    # figure title
    plt.title(title)

    # save figure under reports/figures
    if save_figure_pngs:
        plt.savefig('{}/reports/figures/{}'.format(project_dir, (title + '.png')))

    # show plot
    if show_plots:
        plt.show()


"""
    Plots the values of dict1_to_plot and dict2_to_plot on the same plot where dict1_to_plot
    values are red and dict2_to_plot values are blue
"""
def plot_2_variables(title, dict1_to_plot, dict1_y_axis_label, dict2_to_plot, dict2_y_axis_label):
    t1 = [*dict1_to_plot]
    t2 = [*dict2_to_plot]
    data1 = dict1_to_plot.values()
    data2 = dict2_to_plot.values()
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(dict1_y_axis_label, color=color)
    ax1.plot(t1, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel(dict2_y_axis_label, color=color)
    ax2.plot(t2, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # figure size
    fig.set_size_inches(12, 5)

    # figure title
    plt.title(title)

    # save figure under reports/figures
    if save_figure_pngs:
        plt.savefig('{}/reports/figures/{}'.format(project_dir, (title + '.png')))

    # show plot
    if show_plots:
        plt.show()


"""
    Calculates the population covariance for values x and y
"""
def population_covariance(x, y):
    mean_x = sum(x)/float(len(x))
    mean_y = sum(y)/float(len(y))
    sub_x = [i - mean_x for i in x]
    sub_y = [i - mean_y for i in y]
    numerator = sum([sub_x[i]*sub_y[i] for i in range(len(sub_x))])
    denominator = len(x)
    cov = numerator/denominator
    return cov


def compare_all_coins_overall():
    """
        Compares overall Reddit coin sentiment to actual the overall coin price as a whole
    """
    logger.info('Comparing overall coin sentiment to overall coin prices')

    # convert summarized reddit data (reddit_summary.json) to Python dictionary
    f = open('{}/data/processed/reddit_summary.json'.format(project_dir))
    reddit_summarized = json.load(f)

    # traverse each day in reddit_summarized to obtain the positive, neutral and negative sentiment scores
    logger.info('Parsing reddit sentiment json file')
    positive_score_sums = {}
    neutral_score_sums = {}
    negative_score_sums = {}
    for day_summary_timestamp in reddit_summarized:
        positive_score_sums[datetime.fromtimestamp(int(day_summary_timestamp[:len(day_summary_timestamp) - 3])).replace(hour=0)] = \
            reddit_summarized[day_summary_timestamp]['overall_positivity_sum']
        neutral_score_sums[datetime.fromtimestamp(int(day_summary_timestamp[:len(day_summary_timestamp) - 3])).replace(hour=0)] = \
            reddit_summarized[day_summary_timestamp]['overall_neutrality_sum']
        negative_score_sums[datetime.fromtimestamp(int(day_summary_timestamp[:len(day_summary_timestamp) - 3])).replace(hour=0)] = \
            reddit_summarized[day_summary_timestamp]['overall_negativity_sum']

    # print(positive_score_sums)
    # print(neutral_score_sums)
    # print(negative_score_sums)

    # for each json coin data file in the coin market cap folder fetch coin open prices
    logger.info('Parsing CoinMarketCap price history json files')
    all_coin_open_prices = []
    for coin_data_file in os.listdir('{}/data/raw/coin market cap/'.format(project_dir)):
        if coin_data_file != 'tickers.csv':  # skip tickers.csv file

            # convert convert json file to Python dictionary
            f = open('{}/data/raw/coin market cap/{}'.format(project_dir, coin_data_file))
            prices = json.load(f)

            # for each day fetch the BTC open
            coin_open_prices = {}
            for daily_data_quotes in prices['data']['quotes']:
                year_month_day = daily_data_quotes['timeOpen'][0:10].split('-')
                dt = datetime(int(year_month_day[0]), int(year_month_day[1]), int(year_month_day[2]))

                if dt > datetime(2021, 10, 1):  # only consider days before a specific date
                    coin_open_prices[dt] = daily_data_quotes['quote']['open']

            #print('coin prices: ', coin_open_prices)
            all_coin_open_prices.append(coin_open_prices)

    # calculate overall % change in coin prices for each day
    logger.info('Calculating overall % change in coin prices')
    all_coin_percent_changes = []
    for coin in all_coin_open_prices:
        coin_percent_changes = {}
        temp_list = list(coin)
        for curr_day in coin:
            if coin[curr_day] != 0:  # sometimes the coin value for the day is 0
                # fetch next day key for dictionary
                try:
                    next_day = temp_list[temp_list.index(curr_day) + 1]
                except (ValueError, IndexError):
                    next_day = None

                if next_day is not None:
                    # compute percentage change in value by comparing current day value to next day value
                    percent_increase = (coin[next_day] - coin[curr_day])*100/(coin[curr_day])

                    # print('-----------------------------------------------------------------')
                    # print('current day is ', curr_day, ' with a value of ', coin[curr_day])
                    # print('The next day is : ' + str(next_day), ' with a value of ', coin[next_day])
                    # print('percent change is ', round(percent_increase, 5))

                    # append the percentage change to dictionary
                    coin_percent_changes[curr_day] = percent_increase

        # append percentage changes of the coin to the overall list
        all_coin_percent_changes.append(coin_percent_changes)

    # at this point all_coin_percent_changes is a list of coin dictionaries where
    # the coin dictionaries map percentage changes values to their respective dates
    # print(all_coin_percent_changes)

    # for each date compute the overall percent change for the entire coin market
    days_since_2021_03_1 = list(rrule.rrule(rrule.DAILY, count=500, dtstart=datetime(2021, 3, 1)))
    overall_percent_changes = {}
    for date in days_since_2021_03_1:
        percent_changes_for_that_day = []
        for coin_percent_change_vals in all_coin_percent_changes:
            if date in coin_percent_change_vals:
                percent_changes_for_that_day.append(coin_percent_change_vals[date])

        # after looking at all percent changes for all the coins, we can compute overall percent change
        if percent_changes_for_that_day:  # some days have no data
            overall_percent_change = sum(percent_changes_for_that_day)/len(percent_changes_for_that_day)
            #print('overall percentage change for ', date, ' was ', overall_percent_change)

            overall_percent_changes[date] = overall_percent_change

    logger.info('Plotting results')

    # plot overall coin value percent changes
    plot_single_variable('Overall coin value percent changes per day', overall_percent_changes, 'Overall coin value % change')

    # plot overall positive sentiment values
    plot_single_variable('Overall positive sentiment values per day', positive_score_sums, 'Sentiment Score')

    # plot overall positive sentiment values
    plot_single_variable('Overall neutral sentiment values per day', neutral_score_sums, 'Sentiment Score')

    # plot overall negative sentiment values
    plot_single_variable('Overall negative sentiment values per day', negative_score_sums, 'Sentiment Score')

    # plot overall coin value percent change vs overall positive sentiment for that day
    plot_2_variables('Overall coin value percent change vs Overall positive sentiment for that day',
                     overall_percent_changes, 'Overall % change in price', positive_score_sums, 'Overall positive sentiment score')

    # plot overall coin value percent change vs overall neutral sentiment for that day
    plot_2_variables('Overall coin value percent change vs Overall neutral sentiment for that day',
                     overall_percent_changes, 'Overall % change in price', neutral_score_sums, 'Overall neutral sentiment score')

    # plot overall coin value percent change vs overall negative sentiment for that day
    plot_2_variables('Overall coin value percent change vs Overall negative sentiment for that day',
                     overall_percent_changes, 'Overall % change in price', negative_score_sums, 'Overall negative sentiment score')

    logger.info('Computing covariances')

    # overall % change vs overall positive sentiment covariance calculations
    matching_positive_scores = []
    matching_percent_changes = []
    for date in positive_score_sums:
        if date in overall_percent_changes.keys():  # if date is present in dictionaries
            matching_positive_scores.append(positive_score_sums[date])
            matching_percent_changes.append(overall_percent_changes[date])
    # print('found ', len(matching_percent_changes), ' matching dates')
    print('overall % change vs overall positive sentiment covariance = ',
          population_covariance(matching_positive_scores, matching_percent_changes))
    # logger.info('overall percent change vs overall positive sentiment covariance = ',
    #       population_covariance(matching_positive_scores, matching_percent_changes))

    # overall % change vs overall neutral sentiment covariance calculations
    matching_neutral_scores = []
    matching_percent_changes = []
    for date in neutral_score_sums:
        if date in overall_percent_changes.keys():  # if date is present in dictionaries
            matching_neutral_scores.append(neutral_score_sums[date])
            matching_percent_changes.append(overall_percent_changes[date])
    # print('found ', len(matching_percent_changes), ' matching dates')
    print('overall % change vs overall neutral sentiment covariance = ',
          population_covariance(matching_neutral_scores, matching_percent_changes))
    # logger.info('overall percent change vs overall neutral sentiment covariance = ',
    #             population_covariance(matching_neutral_scores, matching_percent_changes))

    # overall % change vs overall neutral sentiment covariance calculations
    matching_negative_scores = []
    matching_percent_changes = []
    for date in negative_score_sums:
        if date in overall_percent_changes.keys():  # if date is present in dictionaries
            matching_negative_scores.append(negative_score_sums[date])
            matching_percent_changes.append(overall_percent_changes[date])
    # print('found ', len(matching_percent_changes), ' matching dates')
    print('overall % change vs overall negative sentiment covariance = ',
          population_covariance(matching_negative_scores, matching_percent_changes))
    # logger.info('overall percent change vs overall negative sentiment covariance = ',
    #             population_covariance(matching_negative_scores, matching_percent_changes))


"""
    Program main just executes compare_btc() function
"""
if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler('{}/logs/all_coin_sentiment.log'.format(project_dir), mode = 'w'),
                                logging.StreamHandler()
                            ])

        logger.info('Comparing overall sentiment to actual overall coin prices')
        compare_all_coins_overall()
        logger.info('Done')

    except Exception as e:
        logger.error('An Error Occured: {}'.format(e))

