# SYSC 4906 Term Project
By gathering data from reddit we will be analyzing the sentiment of posts in communities that have strong interests in investment, cryptocurrency, and world politics. We will determine if there exists a link between these sentiments and the flucuation of cryptocurrencies, and if a link exists if it can be used to accurately predict future market behaviour as a consequence of social media based mass hysteria among these populations. The code we have compiled for the initial data munging phase can be found at the Github Repository linked below.  

## Getting Started

### Initial Data Munging and Analysis
The files found in src/data can be used for performing intial data analysis:
<br>
<b>src/data/config</b> contains a configuration file that can be used to define several functions:
 - where data from reddit is being pulled from (ie. what subreddit)
 - with what keywords should we focus on (if any keywords are included, otherwise we can use a set of default keywords, or pull all the data)
 - How many days in the past should we pull from
<br><br>

<b>src/data/raw_reddit_data.py</b> using the config file mentioned above, this script will pull data from reddit. To do this it uses a bot, in order to run this code properly a .env file needs to be configured. Please email me (aedynladd@cmail.carleton.ca) for the data necessary for the .env file. An alternative to this file which pulls data from reddit using the official reddit API is to use the file labelled as <b>src/data/raw_reddit_data_pushshift.py</b> which uses data from pushshift - an unofficial reddit repository created to store the data of posts without being restricted by the 1000 limit.

<br><br>
<b>src/data/text_process.py</b> this script will pull all the previously collected data into a single file, perform analysis on sentiment in posts, and organize by the days that posts occured

<br><br>
<b>src/data/summarize_data.py</b> this script creates a summary of all the afformentioned data grouped per day, displaying information such as the combined sentiment, number of posts, and sentiment as it relates to keywords.

<br><br>
<b>src/visualization/all_coin_sentiment.py</b> this script compares the overall coin sentiment on Reddit to the actual coin prices. More specifically it fetches and parses Reddit sentiment values for each day from <b>data/processed/reddit_summary.json</b> along with actual coin prices from json files in <b>a/raw/coin market cap</b>. After the values have been fetched, they are plotted using matplotlib and all plots/figures are saved under <b>reports/figures</b>

<br><br>
<b>src/visualization/btc_sentiment.py</b> this script compares the Bitcoin sentiment on Reddit to the actual Bitcoin prices on CoinMarketCap. More specifically it fetches and parses Reddit Bitcoin sentiment values for each day for the 'BTC' and 'bitcoin' keywords from <b>data/processed/reddit_summary.json</b>. Additionally it also fetches and parses the actual Bitcoin prices from <b>a/raw/coin market cap/Bitcoin.json</b>. After the values have been fetched, they are plotted using matplotlib and all plots/figures are saved under <b>reports/figures</b>.

## Reports and Other Items of Interest
### Project Proposal
https://www.overleaf.com/8239623562pxkkmdjdtbsg

### Progress Report
https://www.overleaf.com/1613467463dczmnhxynwsj

### Dashboard Link
https://aedynladd.github.io/sysc4906-termProject/

### Project Folder Structure
├── LICENSE <br/>
├── Makefile           <- Makefile with commands like `make data` or `make train`  <br/>
├── README.md          <- The top-level README for developers using this project. <br/>
├── data  <br/>
│   ├── external       <- Data from third party sources.  <br/>
│   ├── interim        <- Intermediate data that has been transformed.  <br/>
│   ├── processed      <- The final, canonical data sets for modeling.  <br/>
│   └── raw            <- The original, immutable data dump.  <br/>
│ <br/>
├── docs               <- A default Sphinx project; see sphinx-doc.org for details <br/>
│ <br/>
├── models             <- Trained and serialized models, model predictions, or model summaries <br/>
│ <br/>
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering), <br/>
│                         the creator's initials, and a short `-` delimited description, e.g. <br/>
│                         `1.0-jqp-initial-data-exploration`. <br/>
│ <br/>
├── references         <- Data dictionaries, manuals, and all other explanatory materials. <br/>
│ <br/>
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc. <br/>
│ <br/>
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g. <br/>
│                         generated with `pip freeze > requirements.txt` <br/>
│ <br/>
├── setup.py           <- Make this project pip installable with `pip install -e` <br/>
├── src                <- Source code for use in this project. <br/>
│   ├── __init__.py    <- Makes src a Python module <br/>
│   │ <br/>
│   ├── data           <- Scripts to download or generate data <br/>
|        └── Config    <- Config files for running scripts
│   │ <br/>
│   ├── features       <- Scripts to turn raw data into features for modeling <br/>
│   │ <br/>
│   ├── models         <- Scripts to train models and then use trained models to make <br/>
│   │ <br/>
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations <br/>
│ <br/>
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io <br/>

