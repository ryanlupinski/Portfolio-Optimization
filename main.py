# ---------------------------------------------------------------------------- #
"""
Title: Portfolio Optimization Tool
Author: Ryan Lupinski (https://github.com/ryanlupinski)
Description: This python script automates the investing strategy of Meb Faber's 'Trinity Portfolio'
as described here: https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf
"""
# --------------------------------------------------------------------------- #

# Import Modules ------------------------------------------------------------ #
if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np
    from portfolio import Portfolio
    from processing import Processor
    from pandas.tseries.offsets import BMonthEnd, BDay
else:
    raise Exception("This file was not created to be imported")
# --------------------------------------------------------------------------- #

# Initialize list of ETFs and timeframes ------------------------------------ #
# List of ETFs that make up the portfolio
lstETFs = [
    'MTUM',  # US Stocks Momentum
    'VTV',  # US Stocks Value
    'VEU',  # Foreign Developed Stock
    'VWO',  # Foreign Emerging Stocks
    'VCIT',  # Corporate Bonds
    'VGLT',  # 30Y Bonds
    'BNDX',  # 10Y Foreign Bonds
    'VTIP',  # TIPS
    'DBC',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]

# Define initial timeframes
tsToday = pd.Timestamp(pd.Timestamp.today().date())  # Remove hour/min/sec/ns convert back to timestamp
tsLastTradingDay = pd.Timestamp(Processor.last_trading_day().date())  # Remove hour/min/sec/ns convert back to timestamp
tsTenYears = tsLastTradingDay - BMonthEnd(120)
print(f"Today: {tsToday}")
print(f"Last trading day: {tsLastTradingDay}")
# --------------------------------------------------------------------------- #

# Load or create dataframes of price data ----------------------------------- #
# --------------------------------------------------------------------------- #
"""OPENING PRICE DATA"""
# Check to see if opening price data csv exists in /Data/Dataframes
try:
    path = os.getcwd() + "/Data/Dataframes"
    # If it already exists, load data
    dfOpeningPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfOpeningPriceDataTenYears.csv'),
                                             index_col='Date',
                                             parse_dates=True)
except:
    print('Creating 10 year opening price dataframe')
    # Create dataframe of 10 years of opening price data
    dfOpeningPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                      end_date=tsLastTradingDay, OHLCVAC='Open')
    # Save dataframe of 10 years of opening price date to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    dfOpeningPriceDataTenYears.to_csv(os.path.join(path, r'dfOpeningPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""CLOSING PRICE DATA"""
# Check to see if closing price data csv exists in /Data/Dataframes
try:
    path = os.getcwd() + "/Data/Dataframes"
    # If it already exists, load data
    dfClosingPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'),
                                             index_col='Date',
                                             parse_dates=True)
except:
    print('Creating 10 year closing price dataframe')
    # Create dataframe of 10 years of closing price data
    dfClosingPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                      end_date=tsLastTradingDay, OHLCVAC='Close')
    # Save dataframe of 10 years of closing price date to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""ADJUSTED CLOSE PRICE DATA"""
# Check to see if adjusted closing price data csv exists in /Data/Dataframes
try:
    path = os.getcwd() + "/Data/Dataframes"
    # If it already exists, load data
    dfAdjClosingPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfAdjClosingPriceDataTenYears.csv'),
                                                index_col='Date',
                                                parse_dates=True)
except:
    print('Creating 10 year adjusted closing price dataframe')
    # Create dataframe of 10 years of adjusted closing price data
    dfAdjClosingPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                         end_date=tsLastTradingDay, OHLCVAC='Adj Close')
    # Save dataframe of 10 years of adjusted closing price date to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    dfAdjClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfAdjClosingPriceDataTenYears.csv'), na_rep='nan',
                                         date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""2OO DAY SIMPLE MOVING AVERAGE PRICE DATA"""
# Check to see if 200D SMA data csv exists in /Data/Dataframes
try:
    path = os.getcwd() + "/Data/Dataframes"
    # If it already exists, load data
    df200DSMATenYears = pd.read_csv(os.path.join(path, r'df200DSMATenYears.csv'),
                                    index_col='Date',
                                    parse_dates=True)
except:
    print('Creating 10 year 200D SMA dataframe')
    # Create dataframe of 10 years of 200D SMA data
    df200DSMATenYears = Processor.moving_average(etfs=lstETFs, start_date=tsTenYears, end_date=tsLastTradingDay,
                                                 OHLCVAC='Close', window=200)
    # Save dataframe of 10 years of 200D SMA data to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    df200DSMATenYears.to_csv(os.path.join(path, r'df200DSMATenYears.csv'), na_rep='nan',
                             date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# Load or create dict of returns and ranks dataframes ----------------------- #
"""
Returns and ranks dataframes need a few extra steps of processing before being created.
Price dataframes may have 'NaN' values if the ETF did not exist yet. Returns depend on 
the existence of price data so 'NaN' values are not acceptable. First we must check each
ETF's price dataframe to find the first valid index, and make that valid index our
tsStartDate. To get 1 year of returns data from tsStartDate, we need to roll forward our timestamp
by at least 1 year or 12 business months. The tool uses 13 business months because BMonthEnd() will find
the current month end, so it is possible that taking tsStartDate + BMonthEnd(12) may only return
11 months of data. 13 business months ensures that no price data is 'NaN'. This new timestamp will
become the tsIndexPointer, ie the timestamp from which all price data, calculations, and
portfolio building will begin, because all the data backward by 1 year is valid, and all the data
forward up until tsLastTradingData is valid.
"""
# Initialize start date to data 10 years from last trading day
tsStartDate = tsTenYears
# Check each ETF for first date of adjusted closing price data
# If the first valid index date is after tsStartDate, set tsStartDate to first valid index date
for etf, data in dfAdjClosingPriceDataTenYears.items():
    if data.first_valid_index() > tsStartDate:
        tsStartDate = data.first_valid_index()

print(f'first complete data index is {tsStartDate}')

# roll forward tsStartDate index date ahead 13 business months so return dataframes will have valid data
tsIndexPointer = tsStartDate + BMonthEnd(13)
print(f"The tool will begin at index: {tsIndexPointer}")

# --------------------------------------------------------------------------- #
"""Returns and Ranks dataframes"""
# Check to see if ETF Returns and Ranks data exist in /Data/Dataframes/ETF Returns and Ranks
try:
    path = os.getcwd() + "/Data/Dataframes/ETF Returns and Ranks"
    # If it already exists, load data
    dictOfETFReturnsDataframes = {}
    for etf in lstETFs:
        x = str("".join(['df', etf]))
        df = pd.read_csv(os.path.join(path, f'df{etf}.csv'),
                         index_col='Date',
                         parse_dates=True)
        dictOfETFReturnsDataframes.update({x: df})
except:
    print('Creating Returns and Ranks dataframes')
    # Create dict of dataframes for each ETF's returns and rank
    dictOfETFReturnsDataframes = Processor.returns_and_rank(tsStart=tsIndexPointer,
                                                            tsEnd=tsLastTradingDay,
                                                            dfAdjClosingPrice=dfAdjClosingPriceDataTenYears)
    # save each dataframe in dict to csv
    path = os.getcwd() + "/Data/Dataframes/ETF Returns and Ranks"
    for etf in dictOfETFReturnsDataframes:
        dictOfETFReturnsDataframes[etf].to_csv(os.path.join(path, str(etf) + '.csv'),
                                               na_rep='nan', date_format='%Y-%m-%d %H:%M:%S')

# --------------------------------------------------------------------------- #

# Main ---------------------------------------------------------------------- #
"""
Now that all the dataframes have been created/loaded the tool can check to see if
the loaded dataframes are up to date, ie do they have valid price data and returns up
to tsLastTradingDay.
"""

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW OPENING PRICE DATA NOT CURRENTLY IN DATAFRAME"""
# Find the latest index of dfOpeningPriceDataTenYears
tsLatestOpeningPriceData = dfOpeningPriceDataTenYears.index[-1]

if tsLastTradingDay > tsLatestOpeningPriceData:
    tsLatestOpeningPriceData += BDay(1)  # advance tsLatestOpeningPriceData to next business day so no index overlap
    dfNewOpeningPriceData = Processor.price_data(etfs=lstETFs,
                                                 start_date=tsLatestOpeningPriceData,
                                                 end_date=tsLastTradingDay,
                                                 OHLCVAC='Open')
    dfOpeningPriceDataTenYears = dfOpeningPriceDataTenYears.append(dfNewOpeningPriceData,
                                                                   verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    dfOpeningPriceDataTenYears.to_csv(os.path.join(path, r'dfOpeningPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
    tsLatestOpeningPriceData = dfOpeningPriceDataTenYears.index[-1]  # reset tsLatestOpeningPriceData
else:
    print("dfOpeningPriceDataTenYears is up to date")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW CLOSING PRICE DATA NOT CURRENTLY IN DATAFRAME"""
# Find the latest index of dfClosingPriceDataTenYears
tsLatestClosingPriceData = dfClosingPriceDataTenYears.index[-1]

if tsLastTradingDay > tsLatestClosingPriceData:
    tsLatestClosingPriceData += BDay(1)  # advance tsLatestClosingPriceData to next business day so no index overlap
    dfNewClosingPriceData = Processor.price_data(etfs=lstETFs,
                                                 start_date=tsLatestClosingPriceData,
                                                 end_date=tsLastTradingDay,
                                                 OHLCVAC='Close')
    dfClosingPriceDataTenYears = dfClosingPriceDataTenYears.append(dfNewClosingPriceData,
                                                                   verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
    tsLatestClosingPriceData = dfClosingPriceDataTenYears.index[-1]  # reset tsLatestClosingPriceData
else:
    print("dfClosingPriceDataTenYears is up to date")

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW ADJUSTED CLOSING PRICE DATA NOT CURRENTLY IN DATAFRAME"""
# Find the latest index of dfAdjClosingPriceDataTenYears
tsLatestAdjClosingPriceData = dfAdjClosingPriceDataTenYears.index[-1]

if tsLastTradingDay > tsLatestAdjClosingPriceData:
    tsLatestAdjClosingPriceData += BDay(1)  # advance tsLatestAdjClosingPriceData to next business day so no index overlap
    dfNewAdjClosingPriceData = Processor.price_data(etfs=lstETFs,
                                                    start_date=tsLatestAdjClosingPriceData,
                                                    end_date=tsLastTradingDay,
                                                    OHLCVAC='Adj Close')
    dfAdjClosingPriceDataTenYears = dfAdjClosingPriceDataTenYears.append(dfNewAdjClosingPriceData,
                                                                         verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    dfAdjClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfAdjClosingPriceDataTenYears.csv'), na_rep='nan',
                                         date_format='%Y-%m-%d %H:%M:%S')
    tsLatestAdjClosingPriceData = dfAdjClosingPriceDataTenYears.index[-1]  # reset tsLatestAdjClosingPriceData
else:
    print("dfAdjClosingPriceDataTenYears is up to date")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW 200D SMA DATA NOT CURRENTLY IN DATAFRAME"""
# Find the latest index of df200DSMATenYears
tsLatest200DSMAData = df200DSMATenYears.index[-1]

if tsLastTradingDay > tsLatest200DSMAData:
    tsLatest200DSMAData += BDay(1)  # advance tsLatest200DSMAData to next business day so no index overlap
    tsNew200DSMA = tsLatest200DSMAData - BMonthEnd(24)  # rollback new ts to get enough data for 1,3,6,12 MAs
    dfNew200DSMATenYears = Processor.moving_average(etfs=lstETFs,
                                                    start_date=tsNew200DSMA,
                                                    end_date=tsLastTradingDay,
                                                    OHLCVAC='Close',
                                                    window=200)
    dfNew200DSMATenYears = dfNew200DSMATenYears.loc[tsLatest200DSMAData:]  # splice only new index dates to append
    df200DSMATenYears = df200DSMATenYears.append(dfNew200DSMATenYears, verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    df200DSMATenYears.to_csv(os.path.join(path, r'df200DSMATenYears.csv'), na_rep='nan',
                             date_format='%Y-%m-%d %H:%M:%S')
    tsLatest200DSMAData = df200DSMATenYears.index[-1]  # reset tsLatest200DSMAData
else:
    print("df200DSMATenYears is up to date")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW RETURNS AND RANKS DATA NOT CURRENTLY IN CSV"""
# Find the latest index of dictOfETFReturnsDataframes
# All ETFs will have the same index, so use first key of dictOfETFReturnsDataframes
x = list(dictOfETFReturnsDataframes.keys())[0]
tsLatestReturnsData = dictOfETFReturnsDataframes[x].index[-1]

if tsLastTradingDay > tsLatestReturnsData:
    tsLatestReturnsData += BMonthEnd()  # advance tsLatestReturnsData to next BMonthEnd day so no index overlap
    Processor.returns_and_rank(tsStart=tsLatestReturnsData,
                               tsEnd=tsLastTradingDay,
                               dfAdjClosingPrice=dfAdjClosingPriceDataTenYears,
                               dictOfReturns=dictOfETFReturnsDataframes)
    # save each dataframe in dict to csv
    path = os.getcwd() + "/Data/Dataframes/ETF Returns and Ranks"
    for etf in dictOfETFReturnsDataframes:
        dictOfETFReturnsDataframes[etf].to_csv(os.path.join(path, str(etf) + '.csv'),
                                               na_rep='nan', date_format='%Y-%m-%d %H:%M:%S')
    x = list(dictOfETFReturnsDataframes.keys())[0]
    tsLatestReturnsData = dictOfETFReturnsDataframes[x].index[-1]  # reset tsLatestReturnsData
else:
    print("dictOfETFReturnsDataframes is up to date")
# --------------------------------------------------------------------------- #

# !!! SECTION FOR CREATING CSVS FOR SPREADSHEET !!!
tsIndexDateOneMonth = tsLastTradingDay - BMonthEnd(1)
tsIndexDateThreeMonth = tsLastTradingDay - BMonthEnd(3)
tsIndexDateSixMonth = tsLastTradingDay - BMonthEnd(6)
tsIndexDateOneYear = tsLastTradingDay - BMonthEnd(12)

# Create 1m, 3m, 6m, & 1y dataframes of daily adjusted closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateOneMonth:tsLastTradingDay]
dfETFPriceDataThreeMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateThreeMonth:tsLastTradingDay]
dfETFPriceDataSixMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateSixMonth:tsLastTradingDay]
dfETFPriceDataOneYear = dfAdjClosingPriceDataTenYears.loc[tsIndexDateOneYear:tsLastTradingDay]

# Create dataframes of 200 day simple moving average for all ETFs in portfolio
dfETF200DayMovingAverage = Processor.moving_average(etfs=lstETFs, start_date=tsIndexDateOneYear,
                                                    end_date=tsLastTradingDay, OHLCVAC='Close', window=200)
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
path = os.getcwd() + "/Data/Spreadsheet CSVs"
dfETFPriceDataOneYear.to_csv(os.path.join(path, r'Portfolio 1 Year Closing Price Data.csv'))
dfETF200DayMovingAverageLatest.to_csv(os.path.join(path, r'Portfolio Latest 200D SMA.csv'))
dfTotalReturns.to_csv(os.path.join(path, r'Portfolio Returns.csv'))

print("CSVs created! Add each csv to the appropriate sheet in Portfolio Optimization Tool.xlsx")

# !!! SECTION FOR CREATING PORTFOLIO OBJECT AND BACKTEST !!!
# dict of ETF buy and hold percentages for 1st 50% of portfolio
dictPortfolioBuyAndHold = {
    'MTUM': 0.05,
    'VTV': 0.05,
    'VEU': 0.0675,
    'VWO': 0.0225,
    'VCIT': 0.089,
    'VGLT': 0.0675,
    'BNDX': 0.072,
    'VTIP': 0.009,
    'DBC': 0.025,
    'IAU': 0.025,
    'VNQ': 0.0225
}
# Instantiate the portfolio w/ $10k
portfolio = Portfolio(etfs=lstETFs, portfolioValue=10000)

for etf in lstETFs:
    # Find the $ amount for each ETF for the 50% buy and hold portion
    fltETFDollarAmount = dictPortfolioBuyAndHold[etf] * portfolio.portfolioValue
    # Get opening price for each ETF on the tsIndexPointer date
    fltETFOpeningPrice = Processor.price_data(etfs=etf,
                                              start_date=tsIndexPointer,
                                              end_date=tsIndexPointer,
                                              OHLCVAC='Open')[0]
    intETFShares = int(np.floor(fltETFDollarAmount / fltETFOpeningPrice))
    fltETFBuyAmount = float(fltETFOpeningPrice * intETFShares)
    portfolio.setPortfolioCash(cash_delta=fltETFBuyAmount)
    print(intETFShares)

input("hold:")
