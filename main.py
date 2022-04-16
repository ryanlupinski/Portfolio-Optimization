__author__ = 'ryanlupinski'

import datetime as dt
import os
from typing import List
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay
from dateutil.relativedelta import *

# Define ETFs in Portfolio
portfolio = [
    'MTUM',  # US Stocks Momentum
    'VTV',  # US Stocks Value
    'VEU',  # Foreign Developed Stock
    'VWO',  # Foreign Emerging Stocks
    'VCIT',  # Corporate Bonds
    'VGLT',  # 30Y Bonds
    'BNDX',  # 10Y Foreign Bonds
    'VTIP',  # TIPS
    'VAW',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]

# Define time frames
today = dt.date.today()
one_month = dt.date(today.year, today.month, 1) - relativedelta(months=0, days=0) - BDay()
three_month = dt.date(today.year, today.month, 1) - relativedelta(months=2, days=0) - BDay()
six_month = dt.date(today.year, today.month, 1) - relativedelta(months=5, days=0) - BDay()
one_year = dt.date(today.year, today.month, 1) - relativedelta(months=11, days=0) - BDay()

print(today)
print(one_month)
print(three_month)
print(six_month)
print(one_year)

# Create 1m, 3m, 6m, & 1y data frames of daily closing price for all ETFs
ETF_price_data_one_month = web.DataReader(portfolio, 'yahoo', one_month, today)['Adj Close']
ETF_price_data_three_month = web.DataReader(portfolio, 'yahoo', three_month, today)['Adj Close']
ETF_price_data_six_month = web.DataReader(portfolio, 'yahoo', six_month, today)['Adj Close']
ETF_price_data_one_year = web.DataReader(portfolio, 'yahoo', one_year, today)['Adj Close']
ETF_price_data_latest = ETF_price_data_one_year.tail(1)

# Create data frames of 200 day simple moving average
ETF_price_data_one_year_close = web.DataReader(portfolio, 'yahoo', one_year, today)['Close']
ETF_price_data_200D_SMA = ETF_price_data_one_year_close.rolling(window=200).mean()
ETF_price_data_200D_SMA_latest = ETF_price_data_200D_SMA.tail(1)

# Create CSV in Price Data folder for closing price and 200 day simple moving average
path = r'/Users/ryanlupinski/PycharmProjects/Finance/Trinity Strategy/Price Data'
ETF_price_data_one_year.to_csv(os.path.join(path, r'Portfolio 1 Year Closing Price Data.csv'))
ETF_price_data_200D_SMA_latest.to_csv(os.path.join(path, r'Portfolio Latest 200D SMA.csv'))

# Calculate 1m, 3m, 6m, & 1y returns for all ETFs in portfolio
# 1 month
Portfolio_one_month_daily_return = ETF_price_data_one_month.pct_change()
Portfolio_one_month_cumulative_return = ((1 + Portfolio_one_month_daily_return).cumprod() - 1)
Portfolio_one_month_cumulative_return = Portfolio_one_month_cumulative_return.tail(1)
# 3 month
Portfolio_three_month_daily_return = ETF_price_data_three_month.pct_change()
Portfolio_three_month_cumulative_return = ((1 + Portfolio_three_month_daily_return).cumprod() - 1)
Portfolio_three_month_cumulative_return = Portfolio_three_month_cumulative_return.tail(1)
# 6 month
Portfolio_six_month_daily_return = ETF_price_data_six_month.pct_change()
Portfolio_six_month_cumulative_return = ((1 + Portfolio_six_month_daily_return).cumprod() - 1)
Portfolio_six_month_cumulative_return = Portfolio_six_month_cumulative_return.tail(1)
# 1 year
Portfolio_one_year_daily_return = ETF_price_data_one_year.pct_change()
Portfolio_one_year_cumulative_return = ((1 + Portfolio_one_year_daily_return).cumprod() - 1)
Portfolio_one_year_cumulative_return = Portfolio_one_year_cumulative_return.tail(1)

Returns_concatenated = [
    Portfolio_one_month_cumulative_return,
    Portfolio_three_month_cumulative_return,
    Portfolio_six_month_cumulative_return,
    Portfolio_one_year_cumulative_return
]

Portfolio_returns = pd.concat(Returns_concatenated)
Portfolio_returns = Portfolio_returns.assign(Returns=['1 month', '3 month', '6 month', '1 year'])

# Create CSV in Performance Data folder
path = r'/Users/ryanlupinski/PycharmProjects/Finance/Trinity Strategy/Performance Data'
Portfolio_returns.to_csv(os.path.join(path, r'Portfolio Returns.csv'))
