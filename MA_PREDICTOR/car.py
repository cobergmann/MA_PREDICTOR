import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay
from MA_PREDICTOR.global_vars import STOCKS, MARKET
from datetime import datetime


def get_stock_data(ticker, measure='Close'):
    ''' Will return stock data for a given company.
    measure -> 'Close' or 'Open'
    '''
    stock_price = STOCKS[ticker]
    return stock_price[[measure]]

def get_abnormal_return(stock_df, market_df):
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


def event_horizon(announcement, start, end, returns):

    # Creating helper to memorize original announcement date
    ann_helper = announcement

    # If announcement date is no trading day take nearest available
    for add_day in range(0, 2):
        if ann_helper + BDay(add_day) in returns.index:
            announcement = ann_helper + BDay(add_day)
            break

        # Setting date out of range on purpose
        else:
            announcement -= BDay(3000)

    # Default setup if all is normal
    start_day = announcement - BDay(start)
    end_day = announcement + BDay(end)

    # Iterate backwards in time if start_day is not traded
    for add_day in range(0, 8):
        start_day -= BDay(add_day)
        if start_day in returns.index:
            break

    # Non-trading days: Taking next available trading day
    for add_day in range(0, 8):
        end_day += BDay(add_day)
        if end_day in returns.index:
            break

    # Will return an empty dataframe
    return start_day, end_day


def calculate_car(ticker, announcement, start=1, end=1):

    # Retrieve stock data
    stock = get_stock_data(ticker)

    # Calculate abnormal returns
    returns = get_abnormal_return(stock, MARKET)

    # Define event horizon
    start_day, end_day = event_horizon(announcement, start, end, returns)

    # Calculate CAR
    ar = returns.loc[(returns.index >= start_day) &
                      (returns.index <= end_day)]
    if not ar.empty:
        # CAR is the accumulated abnormal return
        return ar.sum()
    return np.nan


def calculate_ar(ticker, announcement, start=1, end=1):

    # Retrieve stock data
    stock = get_stock_data(ticker)

    # Calculate abnormal returns
    returns = get_abnormal_return(stock, MARKET)

    # Define event horizon
    start_day, end_day = event_horizon(announcement, start, end, returns)

    # Calculate AR
    ar = returns.loc[(returns.index >= start_day)
                          & (returns.index <= end_day)]

    if not ar.empty:
        return ar
    return np.nan
