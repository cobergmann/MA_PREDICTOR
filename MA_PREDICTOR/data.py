import pandas as pd
from datetime import datetime


def get_stock_data():
    # TODO connect Manon's function
    # return stock_dict
    pass


def get_market_data(measure='Close'):
    '''This function cleans the market data (S&P 500).
    Measure can be 'Close' and/or 'Open'.'''

    data = pd.read_csv('raw_data/210906_S&P500_SPX.csv')

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

if __name__ == "__main__":
    # get_stock_data()
    get_market_data(measure='Close')
