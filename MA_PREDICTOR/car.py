import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay
from MA_PREDICTOR.global_vars import STOCKS, MARKET
from datetime import datetime, timedelta


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

    # Memorize original announcement date
    ann_helper = announcement

    # If announcement date is no trading day take nearest available
    for add_day in range(0, 2):
        if ann_helper + timedelta(days=add_day) in returns.index:
            announcement = ann_helper + timedelta(days=add_day)
            break

        # Setting date out of range on purpose
        else:
            announcement -= timedelta(days=3000)

    # Default setup if all is normal
    start_day = announcement - timedelta(days=start)
    end_day = announcement + timedelta(days=end)

    # Iterate backwards in time if start_day is not traded
    for add_day in range(6):
        if start_day in returns.index:
            break
        start_day -= timedelta(days=1)


    # Non-trading days: Taking next available trading day
    for add_day in range(6):
        if end_day in returns.index:
            break
        end_day += timedelta(days=1)

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

    # Check if df is empty or carries NaN values (in case returns not available)
    if not ar.empty and not ar.isnull().values.any():
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

    # Check if df is empty or carries NaN values (in case returns not available)
    if not ar.empty and not ar.isnull().values.any():
        return ar
    return np.nan
