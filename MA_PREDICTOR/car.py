import pandas as pd
from pandas.tseries.offsets import BDay
from global_vars import STOCKS, MARKET
from datetime import datetime


def get_stock_data(ticker, measure='Close'):
    ''' Will return stock data for a given company.
    measure -> 'Close' or 'Open'
    '''
    stock_price = STOCKS[ticker]
    return stock_price[[measure]]

def get_abnormal_return(stock_df, market_df): # we need to save the df above so
    #we can use it here + we need to select only the period of time of interest for market_df.
    '''Returns a dataframe with stock and market returns.'''

    # Stock return
    stock_returns = stock_df.pct_change()
    stock_returns.columns = ['stock_return']

    # Market return
    market_returns = market_df.pct_change()
    market_returns.columns = ['market_return']

    # Merge
    merged = stock_returns.join(market_returns)

    # Company return - market return
    merged['abnormal_return'] = merged.stock_return - merged.market_return

    return merged['abnormal_return']


def event_horizon(announcement, start, end):

    # Transform into business days
    start_day = announcement - BDay(start)

    # Non-trading days (taking the later trading day)
    end_day = announcement + BDay(end + 1) if announcement.weekday() > 4 else announcement + BDay(end)

    return start_day, end_day


def calculate_car(ticker, announcement, start=1, end=1):

    # Retrieve stock data
    stock = get_stock_data(ticker)

    # Calculate abnormal returns
    returns = get_abnormal_return(stock, MARKET)

    # Define event horizon
    start_day, end_day = event_horizon(announcement, start, end)

    # Calculate CAR
    car = returns.loc[(returns.index >= start_day) &
                      (returns.index <= end_day)].sum()

    return car
