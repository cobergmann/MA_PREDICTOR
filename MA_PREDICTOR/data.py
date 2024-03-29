import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
import yfinance as yf
from datetime import datetime
import pickle
from MA_PREDICTOR.car import calculate_car
import os
from MA_PREDICTOR.global_vars import STOCKS


def get_stock_data():

    """First, we load the data and preprocess it."""

    df_initial = pd.read_csv("raw_data/210906_LeWagon_finalproject_v2.csv")
    df_initial = df_initial.rename(columns={'Acquiror Primary Ticker Symbol': 'Acquiror_Primary_Ticker_Symbol',
                                            'Date Announced': 'Date_Announced'})
    df_initial = df_initial.dropna(subset=['Acquiror_Primary_Ticker_Symbol'])
    df_initial['Date_Announced'] = pd.to_datetime(df_initial['Date_Announced'])

    """Then, we create a new dataframe which will determine the right interval of time."""

    df_min_max = df_initial[['Acquiror_Primary_Ticker_Symbol', 'Date_Announced']].copy()
    df_min_max['date_max'] = df_initial['Date_Announced']
    df_restricted = df_min_max.groupby('Acquiror_Primary_Ticker_Symbol').agg({
        "Date_Announced":min,
        "date_max":max})

    df_restricted['30_days_before'] = df_restricted['Date_Announced'] - BDay(30)
    df_restricted['30_days_after'] = df_restricted['date_max'] + BDay(30)

    """We create a list with all the unique ticker which will be the key of our dict."""

    unique_ac_code = df_initial['Acquiror_Primary_Ticker_Symbol'].unique(
    ).tolist()

    """We create two other lists : one will be a list of dataframes which
    corresponds to the stock prices of each company for the interval selected.
    The other will be a list of all the tickers that does not provide stock prices
    through the API."""

    list_df = []
    list_missing = []

    """ Then, we do a for loop that will retrieve the stock prices..."""

    for code in unique_ac_code:
        ticker = yf.Ticker(code)
        date_min = df_restricted.loc[code,
                                     '30_days_before'].strftime("%Y-%m-%d")
        date_max = df_restricted.loc[code,
                                     '30_days_after'].strftime("%Y-%m-%d")
        stock_data = ticker.history(start=date_min,
                                    end=date_max)[['Open', 'Close']]
        if len(stock_data) != 0:
            list_df.append(stock_data)
        else:
            list_missing.append(str(code))

    """...and we need to take the tickers that does not provide information
    from the list of unique ticker in order to modify our dataset."""

    for code in list_missing:
        unique_ac_code.remove(code)

    dictionary = dict(zip(unique_ac_code, list_df))

    """Finally, we save this dataframe as a pickle file...."""

    with open('MA_PREDICTOR/data/stock_data.pkl', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('Saved as stock_data.pkl')

    """...as well as the list of missing tickers."""
    with open('MA_PREDICTOR/data/missing_data.pkl', 'wb') as handle:
        pickle.dump(list_missing, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('Saved as missing_data.pkl')


def get_market_data(measure='Close'):
    '''This function cleans the market data (S&P 500).
    Measure can be 'Close' and/or 'Open'.'''

    data = pd.read_csv('raw_data/210908_S&P500_SPX.csv')

    # Transform date and set as index
    to_date = lambda x: datetime.strptime(x, '%d-%b-%Y')
    data['Exchange Date'] = data['Exchange Date'].apply(to_date)
    data.set_index('Exchange Date', inplace=True)

    # Transform closing price into float
    rem_com = lambda x: x.replace(',', '')
    data["Close"] = data['Close'].apply(rem_com).astype(float)
    data["Open"] = data['Open'].apply(rem_com).astype(float)
    data = data[[measure]]

    # Save as pickle
    data.to_pickle('MA_PREDICTOR/data/clean_market.pkl')
    print('Saved as clean_market.pkl')

def add_car(df):

    # CAR for different event horizons
    event_horizons = [1, 3, 5, 10]

    for horizon in event_horizons:
        df[f'car_{horizon}'] = df.apply(
            lambda row:
                calculate_car(row.acquiror_ticker, row.announcement_date,
                              start=horizon, end=horizon)
                if row.acquiror_ticker in STOCKS
                else np.NaN, # if ticker not in dict put nan
                axis=1)
        print(f'Added car_{horizon} to dataframe.')

    # Name needs to be changed depending on which csv is used
    df.to_csv(f'MA_PREDICTOR/data/ma_data_car.csv',
                  index=False)
    print(f'Added all CARs to dataframe.')


if __name__ == "__main__":
    # get_stock_data()
    # get_market_data(measure='Close')
    data = pd.read_csv('MA_PREDICTOR/data/ma_data.csv',
               parse_dates=['announcement_date'])
    add_car(data)
    #detail_data = pd.read_csv('MA_PREDICTOR/data/ma_detailed_data.csv',
    #                         parse_dates=['announcement_date'])
    #add_car(detail_data)
