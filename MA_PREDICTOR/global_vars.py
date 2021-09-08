import pandas as pd
import os

package_path = os.path.dirname(__file__)
pickle_path = os.path.join(package_path, 'data')

STOCKS = pd.read_pickle(os.path.join(pickle_path, 'stock_data.pkl'))
MARKET = pd.read_pickle(os.path.join(pickle_path, 'clean_market.pkl'))
