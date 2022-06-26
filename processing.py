if __name__ == "__main__":
    raise Exception("This file is not meant to ran by itself")
else:
    import datetime as dt
    import pandas_datareader.data as web
    from pandas.tseries.offsets import BMonthEnd

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
    def price_data(etfs, start_date, end_date, OHLCVAC):
        """
        Returns a dataframe of price data for a list of ETFs over a specific time frame
        :param OHLCVAC: choose 1 item: 'Open', 'High', 'Low', 'Close', 'Volume', or 'Adj Close'
        :param end_date: last day of time frame to return price data
        :param etfs: ETF symbols to get price from
        :param start_date: first day of time frame to return price data
        :return: dataframe of price data
        """
        dfPriceData = web.DataReader(etfs, 'yahoo', start=start_date, end=end_date)[OHLCVAC]
        return dfPriceData

    @staticmethod
    def moving_average(etfs, start_date, end_date, OHLCVAC, window):
        """
        Calculates 200 day moving average for ETFs and returns dataframe of latest average
        for the given time frame
        :param window: int: window of days to calculate average
        :param OHLCVAC: choose 1 item: 'Open', 'High', 'Low', 'Close', 'Volume', or 'Adj Close'
        :param end_date: last day of time frame to return price data
        :param start_date: first day of time frame to return price data
        :param etfs: ETF symbols to get price from
        :return: dataframe of 200 day moving averages for each ETF
        """
        df = web.DataReader(etfs, 'yahoo', start=start_date, end=end_date)[OHLCVAC]
        dfMovingAverage = df.rolling(window=window).mean()
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
