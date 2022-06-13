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
    import pandas_datareader.data as web
    from pandas.tseries.offsets import BDay
    from pandas.tseries.offsets import BMonthEnd
    from dateutil.relativedelta import *
    # from backtest import Portfolio
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
today = dt.date.today()


# --------------------------------------------------------------------------- #

# Processing  --------------------------------------------------------------- #
class Processor:
    @staticmethod
    def time_frame(years, months):
        """
        Returns a business date in the past based on years and months parameter
        time_frame(years=1, months=0) returns the last business day 1 year from today()
        time_frame(years=8, months=1) returns the last business day 8 years and 1 month from today()
        :param years: int, years in the past
        :param months: int, months in the past
        :return: date
        """
        dateReturn = dt.datetime(today.year, today.month, 1) - relativedelta(years=years, months=months) - BDay()
        return dateReturn

    @staticmethod
    def price_data(etfs, time_frame):
        """
        Given a time frame and list of ETFs, returns a dataframe of price data
        returns a dataframe of price data for a list of ETFs over a specific time frame
        :param etfs: ETF symbols to get price from
        :param time_frame: time frame as variable pointing to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
        :return: dataframe of price data
        """
        dfPriceData = web.DataReader(etfs, 'yahoo', start=time_frame, end=lastTradingDayOfMonth)['Adj Close']
        return dfPriceData

    @staticmethod
    def moving_average(etfs, time_frame):
        """
        Calculates 200 day moving average for ETFs and returns dataframe of latest average
        for the given time frame
        :param etfs: ETF symbols to get price from
        :param time_frame: start date of time frame
        :return: dataframe of 200 day moving averages for each ETF
        """
        df = web.DataReader(etfs, 'yahoo', start=time_frame, end=lastTradingDayOfMonth)['Adj Close']
        dfMovingAverage = df.rolling(window=200).mean()
        return dfMovingAverage

    @staticmethod
    def total_returns(df):
        """
        Calculates total return of ETFs for each dataframe
        :param df: dataframe to find total returns
        :return: dataframe of returns
        """
        dfPercentChange = df.pct_change()
        dfCumulativeReturn = ((1 + dfPercentChange).cumprod() - 1)
        dfCumulativeReturnLatest = dfCumulativeReturn.tail(1)
        return dfCumulativeReturnLatest


# Main ---------------------------------------------------------------------- #
# Define time frames
lastTradingDayOfMonth = Processor.time_frame(years=0, months=-1)
oneMonth = Processor.time_frame(years=0, months=0)
threeMonths = Processor.time_frame(years=0, months=2)
sixMonths = Processor.time_frame(years=0, months=5)
oneYear = Processor.time_frame(years=0, months=11)

print(f"The last trading day of the month is {lastTradingDayOfMonth}")
print(f"One month ago was {oneMonth}")
print(f"Three months ago was {threeMonths}")
print(f"Six month ago was {sixMonths}")
print(f"One year ago was {oneYear}")

# Create 1m, 3m, 6m, & 1y data frames of daily closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = Processor.price_data(etfs=lstETFs, time_frame=oneMonth)
dfETFPriceDataThreeMonth = Processor.price_data(etfs=lstETFs, time_frame=threeMonths)
dfETFPriceDataSixMonth = Processor.price_data(etfs=lstETFs, time_frame=sixMonths)
dfETFPriceDataOneYear = Processor.price_data(etfs=lstETFs, time_frame=oneYear)
dfETFPriceDataLatest = dfETFPriceDataOneYear.tail(1)

# Create dataframes of 200 day simple moving average for all ETFs in portfolio
dfETF200DayMovingAverage = Processor.moving_average(etfs=lstETFs, time_frame=oneYear)
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
