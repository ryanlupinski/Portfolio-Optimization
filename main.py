# ---------------------------------------------------------------------------- #
# Title: Portfolio Optimization Tool
# Author: Ryan Lupinski (https://github.com/ryanlupinski)
# Description: This python script automates the investing strategy of Meb Faber's 'Trinity Portfolio'
# as described here: https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf
# --------------------------------------------------------------------------- #

# Import Modules ------------------------------------------------------------ #
if __name__ == "__main__":
    import datetime as dt
    import os
    import pandas as pd
    from portfolio import Portfolio
    from processing import Processor
    from pandas.tseries.offsets import BMonthEnd, BDay
else:
    raise Exception("This file was not created to be imported")
# --------------------------------------------------------------------------- #

# Data ---------------------------------------------------------------------- #
# List of ETFs that make up the portfolio
lstETFs = [
    'MTUM',  # US Stocks Momentum
    'VTV',  # US Stocks Value
    'VEU',  # Foreign Developed Stock
    'VWO',  # Foreign Emerging Stocks
    'VCIT',  # Corporate Bonds
    'VGLT',  # 30Y Bonds
    'BNDX',  # 10Y Foreign BondsPo
    'VTIP',  # TIPS
    'DBC',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]

# --------------------------------------------------------------------------- #

# Main ---------------------------------------------------------------------- #
# Define time frames
today = dt.date.today()
lastTradingDayOfMonth = Processor.last_trading_day()
oneMonth = lastTradingDayOfMonth - BMonthEnd(1)
threeMonths = lastTradingDayOfMonth - BMonthEnd(3)
sixMonths = lastTradingDayOfMonth - BMonthEnd(6)
oneYear = lastTradingDayOfMonth - BMonthEnd(12)

print(f"Today: {today}")
print(f"Last trading day: {lastTradingDayOfMonth}")
print(f"One month from last trading: {oneMonth}")
print(f"Three months from last trading day: {threeMonths}")
print(f"Six month from last trading day: {sixMonths}")
print(f"One year from last trading day: {oneYear}")

# Create 1m, 3m, 6m, & 1y data frames of daily adjusted closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = Processor.price_data(etfs=lstETFs, start_date=oneMonth, end_date=lastTradingDayOfMonth, OHLCVAC='Adj Close')
dfETFPriceDataThreeMonth = Processor.price_data(etfs=lstETFs, start_date=threeMonths, end_date=lastTradingDayOfMonth, OHLCVAC='Adj Close')
dfETFPriceDataSixMonth = Processor.price_data(etfs=lstETFs, start_date=sixMonths, end_date=lastTradingDayOfMonth, OHLCVAC='Adj Close')
dfETFPriceDataOneYear = Processor.price_data(etfs=lstETFs, start_date=oneYear, end_date=lastTradingDayOfMonth, OHLCVAC='Adj Close')
dfETFPriceDataLatest = dfETFPriceDataOneYear.tail(1)

# Create dataframes of 200 day simple moving average for all ETFs in portfolio
dfETF200DayMovingAverage = Processor.moving_average(etfs=lstETFs, start_date=oneYear, end_date=lastTradingDayOfMonth, OHLCVAC='Adj Close', window=200)
dfETF200DayMovingAverageLatest = dfETF200DayMovingAverage.tail(1)

# Calculate 1m, 3m, 6m, & 1y returns for all ETFs in portfolio
dfETFOneMonthTotalReturn = Processor.total_returns(dfETFPriceDataOneMonth)
dfETFThreeMonthTotalReturn = Processor.total_returns(dfETFPriceDataThreeMonth)
dfETFSixMonthTotalReturn = Processor.total_returns(dfETFPriceDataSixMonth)
dfETFOneYearTotalReturn = Processor.total_returns(dfETFPriceDataOneYear)

lstOfTotalReturns = [
    dfETFOneMonthTotalReturn,
    dfETFThreeMonthTotalReturn,
    dfETFSixMonthTotalReturn,
    dfETFOneYearTotalReturn
]

dfTotalReturns = pd.concat(lstOfTotalReturns)
dfTotalReturns = dfTotalReturns.assign(Returns=['1 month', '3 month', '6 month', '1 year'])

# Create csvs for closing price data, 200 day simple moving average data, and returns data
path = os.getcwd() + "/CSVs"
dfETFPriceDataOneYear.to_csv(os.path.join(path, r'Portfolio 1 Year Closing Price Data.csv'))
dfETF200DayMovingAverageLatest.to_csv(os.path.join(path, r'Portfolio Latest 200D SMA.csv'))
dfTotalReturns.to_csv(os.path.join(path, r'Portfolio Returns.csv'))

print("CSVs created! Add each csv to the appropriate sheet in Portfolio Optimization Tool.xlsx")
