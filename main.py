# ---------------------------------------------------------------------------- #
# Title: Portfolio Optimization Tool
# Author: Ryan Lupinski (https://github.com/ryanlupinski)
# Description: This python script automates the investing strategy of Meb Faber's 'Trinity Portfolio'
# as described here: https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf
# --------------------------------------------------------------------------- #

# Import Modules ------------------------------------------------------------ #
if __name__ == "__main__":
    import os
    import pandas as pd
    # from portfolio import Portfolio
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
    'BNDX',  # 10Y Foreign Bonds
    'VTIP',  # TIPS
    'DBC',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]

# Define initial timeframes
tsToday = pd.Timestamp.today().date()  # Remove hour/min/sec/ns
tsToday = pd.Timestamp(tsToday)  # convert back to timestamp
tsLastTradingDay = pd.Timestamp(Processor.last_trading_day().date())
tsTenYears = tsLastTradingDay - BMonthEnd(120)
print(f"Today: {tsToday}")
print(f"Last trading day: {tsLastTradingDay}")

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
                                                      end_date=tsLastTradingDay, OHLCVAC='Adj Close')
    # Save dataframe of 10 years of closing price date to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')

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
                                                 OHLCVAC='Adj Close', window=200)
    # Save dataframe of 10 years of 200D SMA data to /Data/Dataframes
    path = os.getcwd() + "/Data/Dataframes"
    df200DSMATenYears.to_csv(os.path.join(path, r'df200DSMATenYears.csv'), na_rep='nan',
                             date_format='%Y-%m-%d %H:%M:%S')

# Initialize start date to data 10 years from last trading day
tsStartDate = tsTenYears
# Check each ETF for first date of closing price data
# If the first valid index date is after tsStartDate, set tsStartDate to first valid index date
for etf, data in dfClosingPriceDataTenYears.items():
    if data.first_valid_index() > tsStartDate:
        tsStartDate = data.first_valid_index()

print(f'first complete data date is {tsStartDate}')

# roll forward tsStartDate index date ahead 13 business months so return dataframes will have valid data
tsIndexPointer = tsStartDate + BMonthEnd(13)
print(f"The tool will begin at index: {tsIndexPointer}")

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
                                                            dfClosingPrice=dfClosingPriceDataTenYears)
    x = list(dictOfETFReturnsDataframes.keys())[0]
    # save each dataframe in dict to csv
    path = os.getcwd() + "/Data/Dataframes/ETF Returns and Ranks"
    for etf in dictOfETFReturnsDataframes:
        dictOfETFReturnsDataframes[etf].to_csv(os.path.join(path, str(etf) + '.csv'),
                                               na_rep='nan', date_format='%Y-%m-%d %H:%M:%S')

# --------------------------------------------------------------------------- #

# Main ---------------------------------------------------------------------- #
# Find dfClosingPriceDataTenYears last index
tsLatestClosingPriceData = dfClosingPriceDataTenYears.index[-1]

# Find df200DSMATenYears last index
tsLatest200DSMAData = df200DSMATenYears.index[-1]

# Find last index of dictOfETFReturnsDataframes
# All ETFs will have the same index, so use first key of dictOfETFReturnsDataframes
x = list(dictOfETFReturnsDataframes.keys())[0]
tsLatestReturnsData = dictOfETFReturnsDataframes[x].index[-1]

# !!! SECTION FOR NEW CLOSING PRICE DATA NOT CURRENTLY IN CSV !!!
if tsLastTradingDay > tsLatestClosingPriceData:
    tsLatestClosingPriceData += BDay(1)  # advance tsLatestClosingPriceData to next business day so no index overlap
    dfNewClosingPriceData = Processor.price_data(etfs=lstETFs,
                                                 start_date=tsLatestClosingPriceData,
                                                 end_date=tsLastTradingDay,
                                                 OHLCVAC='Adj Close')
    dfClosingPriceDataTenYears = dfClosingPriceDataTenYears.append(dfNewClosingPriceData, verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
    tsLatestClosingPriceData = dfClosingPriceDataTenYears.index[-1]  # reset tsLatestClosingPriceData
else:
    print("dfClosingPriceDataTenYears is up to date")


# !!! SECTION FOR NEW 200D SMA DATA NOT CURRENTLY IN CSV !!!
if tsLastTradingDay > tsLatest200DSMAData:
    tsLatest200DSMAData += BDay(1)  # advance tsLatest200DSMAData to next business day so no index overlap
    tsNew200DSMA = tsLatest200DSMAData - BMonthEnd(24)  # rollback new ts to get enough data for 1,3,6,12 MAs
    dfNew200DSMATenYears = Processor.moving_average(etfs=lstETFs,
                                                    start_date=tsNew200DSMA,
                                                    end_date=tsLastTradingDay,
                                                    OHLCVAC='Adj Close',
                                                    window=200)
    dfNew200DSMATenYears = dfNew200DSMATenYears.loc[tsLatest200DSMAData:]  # splice only new index dates to append
    df200DSMATenYears = df200DSMATenYears.append(dfNew200DSMATenYears, verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes"
    df200DSMATenYears.to_csv(os.path.join(path, r'df200DSMATenYears.csv'), na_rep='nan',
                             date_format='%Y-%m-%d %H:%M:%S')
    tsLatest200DSMAData = df200DSMATenYears.index[-1]  # reset tsLatest200DSMAData
else:
    print("df200DSMATenYears is up to date")

# !!! SECTION FOR NEW RETURNS AND RANKS DATA NOT CURRENTLY IN CSV !!!
while True:
    if tsLastTradingDay > tsLatestReturnsData:
        tsLatestReturnsData = tsLatestReturnsData + BMonthEnd()  # advance tsLatestReturnsData to next BMonthEnd day so no index overlap
        Processor.returns_and_rank(tsStart=tsLatestReturnsData,
                                   tsEnd=tsLastTradingDay,
                                   dfClosingPrice=dfClosingPriceDataTenYears,
                                   dictOfReturns=dictOfETFReturnsDataframes)
        x = list(dictOfETFReturnsDataframes.keys())[0]
        # save each dataframe in dict to csv
        path = os.getcwd() + "/Data/Dataframes/ETF Returns and Ranks"
        for etf in dictOfETFReturnsDataframes:
            dictOfETFReturnsDataframes[etf].to_csv(os.path.join(path, str(etf) + '.csv'),
                                                   na_rep='nan', date_format='%Y-%m-%d %H:%M:%S')
        tsLatestReturnsData = dictOfETFReturnsDataframes[x].index[-1]  # reset tsLatestReturnsData
    else:
        print("dictOfETFReturnsDataframes is up to date")
        break

tsIndexDateOneMonth = tsLastTradingDay - BMonthEnd(1)
tsIndexDateThreeMonth = tsLastTradingDay - BMonthEnd(3)
tsIndexDateSixMonth = tsLastTradingDay - BMonthEnd(6)
tsIndexDateOneYear = tsLastTradingDay - BMonthEnd(12)

# Create 1m, 3m, 6m, & 1y data frames of daily adjusted closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = dfClosingPriceDataTenYears.loc[tsIndexDateOneMonth:tsLastTradingDay]
dfETFPriceDataThreeMonth = dfClosingPriceDataTenYears.loc[tsIndexDateThreeMonth:tsLastTradingDay]
dfETFPriceDataSixMonth = dfClosingPriceDataTenYears.loc[tsIndexDateSixMonth:tsLastTradingDay]
dfETFPriceDataOneYear = dfClosingPriceDataTenYears.loc[tsIndexDateOneYear:tsLastTradingDay]
dfETFPriceDataLatest = dfETFPriceDataOneYear.tail(1)

# Create dataframes of 200 day simple moving average for all ETFs in portfolio
dfETF200DayMovingAverage = Processor.moving_average(etfs=lstETFs, start_date=tsIndexDateOneYear, end_date=tsLastTradingDay, OHLCVAC='Adj Close', window=200)
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
