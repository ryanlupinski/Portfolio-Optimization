if __name__ == "__main__":
    raise Exception("This file is not meant to ran by itself")
else:
    import datetime as dt
    import pandas_datareader.data as web
    from pandas.tseries.offsets import BDay, BMonthEnd
    from dateutil.relativedelta import *

# Data ---------------------------------------------------------------------- #
today = dt.date.today()


# Processing  --------------------------------------------------------------- #
class Processor:
    @staticmethod
    def last_trading_day():
        """
        This function checks today.day and today.month
        against lastTradingDayOfMonth.day and lastTradingDayOfMonth.Month
        To set lastTradingDayOfMonth to correct day.
        :return:lastTradingDayOfMonth
        """
        lastTradingDayOfMonth = today + BMonthEnd(0)
        if today.day < lastTradingDayOfMonth.day or today.month != lastTradingDayOfMonth.month:
            lastTradingDayOfMonth = today + BMonthEnd(-1)
        else:
            lastTradingDayOfMonth = today + BMonthEnd(0)

        return lastTradingDayOfMonth

    @staticmethod
    def price_data(etfs, time_frame):
        """
        Given a time frame and list of ETFs, returns a dataframe of price data
        returns a dataframe of price data for a list of ETFs over a specific time frame
        :param etfs: ETF symbols to get price from
        :param time_frame: time frame as variable pointing to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
        :return: dataframe of price data
        """
        lastTradingDayOfMonth = Processor.last_trading_day()
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
        lastTradingDayOfMonth = Processor.last_trading_day()
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
