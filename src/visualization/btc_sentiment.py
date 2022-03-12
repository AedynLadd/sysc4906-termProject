
import json
import logging
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from dateutil import rrule

"""
    btc_sentiment.py looks at the Bitcoin sentiment on Reddit by
    fetching sentiment scores for the 'BTC' and 'bitcoin' keywords and
    then plots the comparison of those values to the actual Bitcoin prices 
    on CoinMarketCap using matplotlib
"""

logger = logging.getLogger('btc_sentiment')
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


def compare_btc():
    """
        Compares Bitcoin sentiment for 'BTC' and 'bitcoin' keywords to actual the Bitcoin price
    """
    logger.info('Comparing BTC sentiment to BTC prices')

    # convert summarized reddit data (reddit_summary.json) to Python dictionary
    f = open('{}/data/processed/reddit_summary.json'.format(project_dir))
    reddit_summarized = json.load(f)

    # for each day summary fetch the sentiment scores for 'BTC' and 'bitcoin' keywords
    btc_scores = {}
    bitcoin_scores = {}
    for day_summary_timestamp in reddit_summarized:
        for keyword in reddit_summarized[day_summary_timestamp]['keyword_based_sentiment']:
            if keyword == 'BTC':
                btc_scores[datetime.fromtimestamp(int(day_summary_timestamp[:len(day_summary_timestamp) - 3])).replace(hour=0)] = \
                    reddit_summarized[day_summary_timestamp]['keyword_based_sentiment'][keyword]['sentiment']
            elif keyword == 'bitcoin':
                bitcoin_scores[datetime.fromtimestamp(int(day_summary_timestamp[:len(day_summary_timestamp) - 3])).replace(hour=0)] = \
                    reddit_summarized[day_summary_timestamp]['keyword_based_sentiment'][keyword]['sentiment']

    # print('btc scores: ', btc_scores)
    # print('bitcoin scores: ', bitcoin_scores)

    # convert CoinMarketCap's data (Bitcoin.json) to Python dictionary
    f = open('{}/data/raw/coin market cap/Bitcoin.json'.format(project_dir))
    bitcoin_price = json.load(f)

    # for each day fetch the BTC open
    btc_prices = {}
    for daily_data_quotes in bitcoin_price['data']['quotes']:
        year_month_day = daily_data_quotes['timeOpen'][0:10].split('-')
        dt = datetime(int(year_month_day[0]), int(year_month_day[1]), int(year_month_day[2]))
        if dt > datetime(2021, 10, 1):  # only consider days before a specific date
            btc_prices[dt] = daily_data_quotes['quote']['open']
    # print('bitcoin prices: ', btc_prices)

    # plot 'BTC' keyword sentiment scores
    plot_single_variable('\'BTC\' keyword sentiment scores', btc_scores, 'Sentiment Score')

    # plot 'bitcoin' keyword sentiment scores
    plot_single_variable('\'bitcoin\' keyword sentiment scores', bitcoin_scores, 'Sentiment Score')

    # plot BTC prices
    plot_single_variable('Actual bitcoin prices', btc_prices, 'Sentiment Score')

    # Plot 'BTC' keyword sentiment score vs bitcoin prices
    plot_2_variables('\'BTC\' keyword sentiment (red) vs Bitcoin price (blue)', btc_scores, 'Sentiment Score', btc_prices, 'Bitcoin price')

    # Plot 'bitcoin' keyword sentiment score vs bitcoin prices
    plot_2_variables('\'bitcoin\' keyword sentiment (red) vs Bitcoin price (blue)', bitcoin_scores, 'Sentiment Score', btc_prices, 'Bitcoin price')

    # Plot 'BTC' + 'bitcoin' keywords sentiment score vs bitcoin prices
    days_since_2021_09_1 = list(rrule.rrule(rrule.DAILY,count=500,dtstart=datetime(2021, 9, 1)))
    summed_vals = {}
    for date in days_since_2021_09_1:
        sum = 0
        if date in btc_scores:
            sum += btc_scores[date]
        if date in bitcoin_scores:
            sum += bitcoin_scores[date]
        summed_vals[date] = sum

    # remove days with no CoinMarketCap data
    dates_to_pop = []
    for date in summed_vals:
        if date > datetime(2022, 4, 1):
            dates_to_pop.append(date)
    for date in dates_to_pop:
        summed_vals.pop(date)

    plot_2_variables('\'bitcoin\' + \'BTC\' keyword sentiments (red) vs bitcoin price (blue)', summed_vals, '\'bitcoin\' + \'BTC\' keyword sentiments', btc_prices, 'bitcoin price')


"""
    Program main just executes compare_btc() function
"""
if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler('{}/logs/btc_sentiment.log'.format(project_dir), mode = 'w'),
                                logging.StreamHandler()
                            ])

        logger.info('Comparing Bitcoin sentiment to actual Bitcoin price')
        compare_btc()
        logger.info('Done')

    except Exception as e:
        logger.error('An Error Occured: {}'.format(e))

