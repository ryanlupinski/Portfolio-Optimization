if __name__ == "__main__":
    raise Exception("This file is not meant to ran by itself")
else:
    import pandas_datareader.data as web
    import pandas as pd
    from pandas.tseries.offsets import BMonthEnd

# Data ---------------------------------------------------------------------- #
tsToday = pd.Timestamp.today()
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
        lastTradingDayOfMonth = tsToday + BMonthEnd(0)
        if tsToday.day < lastTradingDayOfMonth.day or tsToday.month != lastTradingDayOfMonth.month:
            lastTradingDayOfMonth = tsToday + BMonthEnd(-1)
        else:
            lastTradingDayOfMonth = tsToday + BMonthEnd(0)

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
        Calculates 200 day moving average for ETFs and returns dataframe of the latest average
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

    @staticmethod
    def average_etf_returns(etf, df1M, df3M, df6M, df12M):
        """
        Transposes ETF returns from columns to rows, calculates averages,
        and adds new column with that average
        :param etf: ETF from lstETFs
        :param df1M: 1 month ETF total return df
        :param df3M: 3 month ETF total return df
        :param df6M: 6 month ETF total return df
        :param df12M: 12 month ETF total return df
        :return:
        """
        # Split/transpose columns of returns dfs and create new df for ETF
        df = pd.DataFrame(
            data={
                f'{etf}_1M': df1M[etf],
                f'{etf}_3M': df3M[etf],
                f'{etf}_6M': df6M[etf],
                f'{etf}_12M': df12M[etf]
            },
            index=df1M.index
        )
        # find average of each row and add new column
        df[f'{etf}_avg'] = df.mean(axis=1)
        return df

    @staticmethod
    def dict_of_averages_ranked(lstETFs, dictDF):
        """
        NEED INFO HERE
        :param lstETFs:
        :param dictDF:
        :return:
        """
        d = {}
        for etf in lstETFs:
            d.update({f'{etf}_rank': dictDF[f'df{etf}'][f'{etf}_avg'][0]})
        dictRanked = {key: rank for rank, key in enumerate(sorted(d, key=d.get, reverse=True), 1)}
        return dictRanked

    @staticmethod
    def add_rank_to_dict_of_returns(lstETFs, dictDF, rankDF):
        """
        NEED INFO HERE
        :param lstETFs:
        :param dictDF:
        :param rankDF:
        :return:
        """
        for etf in lstETFs:
            dictDF[f'df{etf}'][f'{etf}_rank'] = rankDF[f'{etf}_rank']
        return dictDF

    @staticmethod
    def returns_and_rank(tsStart, tsEnd, dfAdjClosingPrice, dictOfReturns=None):
        while True:
            if tsEnd >= tsStart:
                # Establish 1,3,6,12 month timestamps in the past from indexDate
                tsIndexDateOneMonth = tsStart - BMonthEnd(1)
                tsIndexDateThreeMonth = tsStart - BMonthEnd(3)
                tsIndexDateSixMonth = tsStart - BMonthEnd(6)
                tsIndexDateOneYear = tsStart - BMonthEnd(12)

                # Create dfs of price data for each timeframe to be used for return data
                dfETFPriceDataOneMonth = dfAdjClosingPrice.loc[tsIndexDateOneMonth:tsStart]
                dfETFPriceDataThreeMonth = dfAdjClosingPrice.loc[tsIndexDateThreeMonth:tsStart]
                dfETFPriceDataSixMonth = dfAdjClosingPrice.loc[tsIndexDateSixMonth:tsStart]
                dfETFPriceDataOneYear = dfAdjClosingPrice.loc[tsIndexDateOneYear:tsStart]

                # Get df of 1,3,6,12 month returns
                dfETFOneMonthTotalReturn = Processor.total_returns(dfETFPriceDataOneMonth)
                dfETFThreeMonthTotalReturn = Processor.total_returns(dfETFPriceDataThreeMonth)
                dfETFSixMonthTotalReturn = Processor.total_returns(dfETFPriceDataSixMonth)
                dfETFOneYearTotalReturn = Processor.total_returns(dfETFPriceDataOneYear)

                # Create a dict of dataframes of ETF returns + averages
                # If there is no dict of returns and rank data, create dict of empty dataframes
                if dictOfReturns is None:
                    dictOfReturns = {'dfMTUM': pd.DataFrame(),
                                     'dfVTV': pd.DataFrame(),
                                     'dfVEU': pd.DataFrame(),
                                     'dfVWO': pd.DataFrame(),
                                     'dfVCIT': pd.DataFrame(),
                                     'dfVGLT': pd.DataFrame(),
                                     'dfBNDX': pd.DataFrame(),
                                     'dfVTIP': pd.DataFrame(),
                                     'dfDBC': pd.DataFrame(),
                                     'dfIAU': pd.DataFrame(),
                                     'dfVNQ': pd.DataFrame()
                                     }
                # Create temp dict for loading new returns and ranks dataframes
                dictTemp = {}
                for etf in lstETFs:
                    x = str("".join(['df', etf]))
                    df = Processor.average_etf_returns(etf=etf,
                                                       df1M=dfETFOneMonthTotalReturn,
                                                       df3M=dfETFThreeMonthTotalReturn,
                                                       df6M=dfETFSixMonthTotalReturn,
                                                       df12M=dfETFOneYearTotalReturn)
                    # load etf returns in temp dict
                    dictTemp.update({x: df})

                # Create a sorted dict of numeric rank of ETFs return
                dictOfAveragesRanked = Processor.dict_of_averages_ranked(lstETFs=lstETFs, dictDF=dictTemp)

                # add ranks to new column in each dataframe
                dictTemp = Processor.add_rank_to_dict_of_returns(lstETFs=lstETFs,
                                                                 dictDF=dictTemp,
                                                                 rankDF=dictOfAveragesRanked)

                # append each dataframe in dict with new returns and ranks data
                for key in dictOfReturns:
                    dictOfReturns[key] = dictOfReturns[key].append(dictTemp[key], verify_integrity=True)
                tsStart = tsStart + BMonthEnd(1)
            else:
                break
        return dictOfReturns
