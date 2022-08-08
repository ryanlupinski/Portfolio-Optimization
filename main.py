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
    from portfolio import Portfolio
    from processing import Processor
    from pandas.tseries.offsets import BMonthEnd, BDay
    import matplotlib.pyplot as plt
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
# Check to see if opening price data csv exists in /Data/Dataframes/Price Data
try:
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    # If it already exists, load data
    dfOpeningPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfOpeningPriceDataTenYears.csv'),
                                             index_col='Date',
                                             parse_dates=True)
except:
    print('Creating 10 year opening price dataframe')
    # Create dataframe of 10 years of opening price data
    dfOpeningPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                      end_date=tsLastTradingDay, OHLCVAC='Open')
    # Save dataframe of 10 years of opening price date to /Data/Dataframes/Price Data
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    dfOpeningPriceDataTenYears.to_csv(os.path.join(path, r'dfOpeningPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""CLOSING PRICE DATA"""
# Check to see if closing price data csv exists in /Data/Dataframes/Price Data
try:
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    # If it already exists, load data
    dfClosingPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'),
                                             index_col='Date',
                                             parse_dates=True)
except:
    print('Creating 10 year closing price dataframe')
    # Create dataframe of 10 years of closing price data
    dfClosingPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                      end_date=tsLastTradingDay, OHLCVAC='Close')
    # Save dataframe of 10 years of closing price date to /Data/Dataframes/Price Data
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""ADJUSTED CLOSE PRICE DATA"""
# Check to see if adjusted closing price data csv exists in /Data/Dataframes/Price Data
try:
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    # If it already exists, load data
    dfAdjClosingPriceDataTenYears = pd.read_csv(os.path.join(path, r'dfAdjClosingPriceDataTenYears.csv'),
                                                index_col='Date',
                                                parse_dates=True)
except:
    print('Creating 10 year adjusted closing price dataframe')
    # Create dataframe of 10 years of adjusted closing price data
    dfAdjClosingPriceDataTenYears = Processor.price_data(etfs=lstETFs, start_date=tsTenYears,
                                                         end_date=tsLastTradingDay, OHLCVAC='Adj Close')
    # Save dataframe of 10 years of adjusted closing price date to /Data/Dataframes/Price Data
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    dfAdjClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfAdjClosingPriceDataTenYears.csv'), na_rep='nan',
                                         date_format='%Y-%m-%d %H:%M:%S')
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""2OO DAY SIMPLE MOVING AVERAGE PRICE DATA"""
# Check to see if 200D SMA data csv exists in /Data/Dataframes/Price Data
try:
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    # If it already exists, load data
    df200DSMATenYears = pd.read_csv(os.path.join(path, r'df200DSMATenYears.csv'),
                                    index_col='Date',
                                    parse_dates=True)
except:
    print('Creating 10 year 200D SMA dataframe')
    # Create dataframe of 10 years of 200D SMA data
    df200DSMATenYears = Processor.moving_average(etfs=lstETFs, start_date=tsTenYears, end_date=tsLastTradingDay,
                                                 OHLCVAC='Close', window=200)
    # Save dataframe of 10 years of 200D SMA data to /Data/Dataframes/Price Data
    path = os.getcwd() + "/Data/Dataframes/Price Data"
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
    path = os.getcwd() + "/Data/Dataframes/Price Data"
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
    path = os.getcwd() + "/Data/Dataframes/Price Data"
    dfClosingPriceDataTenYears.to_csv(os.path.join(path, r'dfClosingPriceDataTenYears.csv'), na_rep='nan',
                                      date_format='%Y-%m-%d %H:%M:%S')
    tsLatestClosingPriceData = dfClosingPriceDataTenYears.index[-1]  # reset tsLatestClosingPriceData
else:
    print("dfClosingPriceDataTenYears is up to date")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""SECTION FOR NEW ADJUSTED CLOSING PRICE DATA NOT CURRENTLY IN DATAFRAME"""
# Find the latest index of dfAdjClosingPriceDataTenYears
tsLatestAdjClosingPriceData = dfAdjClosingPriceDataTenYears.index[-1]

if tsLastTradingDay > tsLatestAdjClosingPriceData:
    # advance tsLatestAdjClosingPriceData to next business day so no index overlap
    tsLatestAdjClosingPriceData += BDay(1)
    dfNewAdjClosingPriceData = Processor.price_data(etfs=lstETFs,
                                                    start_date=tsLatestAdjClosingPriceData,
                                                    end_date=tsLastTradingDay,
                                                    OHLCVAC='Adj Close')
    dfAdjClosingPriceDataTenYears = dfAdjClosingPriceDataTenYears.append(dfNewAdjClosingPriceData,
                                                                         verify_integrity=True)
    path = os.getcwd() + "/Data/Dataframes/Price Data"
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
    path = os.getcwd() + "/Data/Dataframes/Price Data"
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

# CSVs for Portfolio Optimization Tool.xlsx --------------------------------- #
""" 
The following CSVs are created in this section
1. Portfolio Last Trading Day Closing Price Data.csv
2. Portfolio Last Trading Day 200D SMA.csv
3. Portfolio Latest Returns.csv

The CSVs must be manually loaded into Portfolio Optimization Tool.xlsx in the
appropriate sheet. Future versions of this tool will automatically load the CSV
data into the appropriate sheet/section. Issues involving the loss of charts in the
spreadsheet currently prevent this from being automated.
"""

# --------------------------------------------------------------------------- #
"""CLOSING PRICE DATA FOR LAST TRADING DAY"""
path = os.getcwd() + "/Data/Spreadsheet CSVs"
dfClosingPriceDataTenYears.tail(1).to_csv(os.path.join(path, r'Portfolio Last Trading Day Closing Price Data.csv'))
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""200 DAY SIMPLE MOVING AVERAGE PRICE DATA FOR LAST TRADING DAY"""
path = os.getcwd() + "/Data/Spreadsheet CSVs"
df200DSMATenYears.tail(1).to_csv(os.path.join(path, r'Portfolio Last Trading Day 200D SMA.csv'))
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""RETURNS DATA FOR 1, 3, 6, 12 MONTHS FROM LAST TRADING DAT"""
tsIndexDateOneMonth = tsLastTradingDay - BMonthEnd(1)
tsIndexDateThreeMonth = tsLastTradingDay - BMonthEnd(3)
tsIndexDateSixMonth = tsLastTradingDay - BMonthEnd(6)
tsIndexDateOneYear = tsLastTradingDay - BMonthEnd(12)

# Create 1m, 3m, 6m, & 1y dataframes of daily adjusted closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateOneMonth:tsLastTradingDay]
dfETFPriceDataThreeMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateThreeMonth:tsLastTradingDay]
dfETFPriceDataSixMonth = dfAdjClosingPriceDataTenYears.loc[tsIndexDateSixMonth:tsLastTradingDay]
dfETFPriceDataOneYear = dfAdjClosingPriceDataTenYears.loc[tsIndexDateOneYear:tsLastTradingDay]

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

path = os.getcwd() + "/Data/Spreadsheet CSVs"
dfTotalReturns.to_csv(os.path.join(path, r'Portfolio Latest Returns.csv'))
# --------------------------------------------------------------------------- #

print("CSVs created! Add each csv to the appropriate sheet in Portfolio Optimization Tool.xlsx")

# --------------------------------------------------------------------------- #
# Portfolio object and backtester ------------------------------------------- #
"""
This section will create a portfolio object from the Portfolio class.
The portfolio object has 1 attribute, a dataframe, shown below.
******************************************************************************************************************
self.__portfolioAssets : DataFrame =
    Date                Cash       ETF1_shares     ETF1_close   ETFn_shares     ETFn_close      Portfolio Value
    YYYY-MM-DD          float      int             float        int             float           float
******************************************************************************************************************
The portfolio object is instantiated with a list of etfs, a portfolio value, and a start date. The backtester will
loop through index dates and add rows of data by buying and selling shares at the open, updating closing prices,
and calculating the Portfolio Value by adding cash + sum(etf shares * etf prices). The tool will start at 
tsIndexPointer and add rows of closing price data for each business day, buy and sell shares at the open on the 
first business day of the month, and calculate the Portfolio Value on each close until tsIndexPointer is 
incremented to tsLastTradingDay. The script will save the dataframe of portfolioAssets so that it can be reloaded, 
and any new data from trading days not yet saved can be added to the dataframe.
"""
# --------------------------------------------------------------------------- #
"""PORTFOLIO DATAFRAME"""
# Check to see if portfolio assets csv exists in /Data/Portfolio Data
try:
    path = os.getcwd() + "/Data/Portfolio Data"
    optimizedPortfolioDataframe = pd.read_csv(os.path.join(path, r'optimizedPortfolio.csv'),
                                              index_col='Date',
                                              parse_dates=True)
    # Find latest date of portfolio assets dataframe
    tsOptimizedPortfolioLastDate = optimizedPortfolioDataframe.index[-1]
    # create optimizedPortfolio object
    optimizedPortfolio = Portfolio(etfs=lstETFs,
                                   portfolioValue=10000.00,
                                   startDate=tsOptimizedPortfolioLastDate,
                                   data=optimizedPortfolioDataframe)
    # check to see if portfolio assets csv is up to date

except:
    print('Creating optimized portfolio object')
    # Instantiate optimizedPortfolio with $10,000 on tsIndexPointer date
    optimizedPortfolioDataframe = None
    optimizedPortfolio = Portfolio(etfs=lstETFs,
                                   portfolioValue=10000.00,
                                   startDate=tsIndexPointer,
                                   data=optimizedPortfolioDataframe)
    # save optimizedPortfolio to /Data/Portfolio Data
    path = os.getcwd() + "/Data/Portfolio Data"
    optimizedPortfolioDataframe = optimizedPortfolio.portfolioAssets
    optimizedPortfolioDataframe.to_csv(os.path.join(path, r'optimizedPortfolio.csv'), na_rep='nan',
                                       date_format='%Y-%m-%d %H:%M:%S')

# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
"""PORTFOLIO DIVIDENDS"""
# Check to see if ETF dividends data exists in /Data/Portfolio Data/Dividends
try:
    path = os.getcwd() + "/Data/Portfolio Data/Dividends"
    dictOfETFDividends = {}
    for etf in lstETFs:
        x = str("".join(['df', etf, '_div']))
        df = pd.read_csv(os.path.join(path, f'df{etf}_dividends.csv'),
                         index_col='Date',
                         parse_dates=True)
        dictOfETFDividends.update({x: df})
except:
    # create dictOfETFDividends
    dictOfETFDividends = Processor.dividends(tsStart=tsIndexPointer,
                                             tsEnd=tsLastTradingDay)
    path = os.getcwd() + "/Data/Portfolio Data/Dividends"
    for etf in dictOfETFDividends:
        dictOfETFDividends[etf].to_csv(os.path.join(path, str('df') + str(etf) + '_dividends.csv'),
                                       na_rep='nan', date_format='%Y-%m-%d %H:%M:%S')

# --------------------------------------------------------------------------- #

while True:
    # if the last index in the portfolioAssets dataframe is earlier than
    # the last trading day enter first loop
    if tsLastTradingDay > optimizedPortfolio.get_last_index():
        # set tsIndexPointer to optimizedPortfolio.portfolioAssets.index[-1]
        tsIndexPointer = optimizedPortfolio.get_last_index()
        tsFindIndex = dfClosingPriceDataTenYears.index[0]
        try:
            iNext -= 1
        except:
            iNext = 0

        while True:
            if tsIndexPointer == dfClosingPriceDataTenYears.index[iNext]:
                tsNextDay = dfClosingPriceDataTenYears.index[iNext+1]
                break
            else:
                iNext += 1

        dictNextDay = {'Date': [tsNextDay],
                       'Cash': [optimizedPortfolio.portfolioAssets.at[tsIndexPointer, 'Cash']]}
        for i in lstETFs:
            dictNextDay.update({f'{i}_shares': optimizedPortfolio.portfolioAssets.at[tsIndexPointer, f'{i}_shares']})
            dictNextDay.update({f'{i}_close': optimizedPortfolio.portfolioAssets.at[tsIndexPointer, f'{i}_close']})
        dictNextDay.update({'Portfolio Value': optimizedPortfolio.portfolioAssets.at[tsIndexPointer,'Portfolio Value']})
        dfNextDay = pd.DataFrame(data=dictNextDay).set_index('Date')
        optimizedPortfolio.add_row_to_dataframe(dfNextDay)

        # check to see if tsIndexPointer is end of month
        tsBMonthEndCheck = tsIndexPointer + BMonthEnd(0)
        if tsIndexPointer == tsBMonthEndCheck:
            # add $100 to account at end of month
            optimizedPortfolio.portfolioAssets.at[tsNextDay, 'Cash'] += 100.00
            optimizedPortfolio.portfolio_closing_value(date=tsNextDay, etfs=lstETFs)
            dictBuyAndHoldPercentages = {
                'MTUM':  0.05,
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

            # check each ETF's rank and close vs. 200D SMA
            for etf in lstETFs:
                # if etf is top 5 rank, and closing price above 200D SMA add 10% to dictBuyAndHoldPercentages
                if dictOfETFReturnsDataframes[f'df{etf}'].at[tsIndexPointer, f'{etf}_rank'] < 6 and \
                        dfClosingPriceDataTenYears.at[tsIndexPointer, f'{etf}'] > \
                        df200DSMATenYears.at[tsIndexPointer, f'{etf}']:
                    dictBuyAndHoldPercentages[f'{etf}'] += 0.1
            for etf in lstETFs:
                # check how many shares the portfolio already has
                intCurrentShares = optimizedPortfolio.portfolioAssets.at[tsIndexPointer, f'{etf}_shares']
                # calculate dollar amount of each ETF to buy based on dictBuyAndHoldPercentages
                intNewETFDollarAmount = (optimizedPortfolio.portfolioAssets.at[tsIndexPointer, f'Portfolio Value'] *
                                         dictBuyAndHoldPercentages[f'{etf}'])
                # calculate the number of shares to buy rounded down
                intNewShares = int(intNewETFDollarAmount / dfOpeningPriceDataTenYears.at[tsIndexPointer, f'{etf}'])
                # calculate shares delta
                intSharesDelta = intCurrentShares - intNewShares
                if intSharesDelta != 0:
                    # if the current shares owned is less than the new shares, buy shares
                    if intCurrentShares < intNewShares:
                        # buy dollar amount at open
                        intBuyShares = abs(intSharesDelta)
                        fltETFOpenBuy = dfOpeningPriceDataTenYears.at[tsNextDay, f'{etf}'] * intBuyShares
                        optimizedPortfolio.buy_shares_at_open(date=tsNextDay,
                                                              etf=etf,
                                                              shares=intBuyShares,
                                                              cost=fltETFOpenBuy)

                    else:
                        # sell dollar amount at open
                        intSellShares = abs(intSharesDelta)
                        fltETFOpenSell = dfOpeningPriceDataTenYears.at[tsNextDay, f'{etf}'] * intSellShares
                        optimizedPortfolio.sell_shares_at_open(date=tsNextDay,
                                                               etf=etf,
                                                               shares=intSellShares,
                                                               cost=fltETFOpenSell)
                # update closing price for each etf
                optimizedPortfolio.update_closing_price(date=tsNextDay,
                                                        etf=etf,
                                                        price=dfClosingPriceDataTenYears.at[tsNextDay, f'{etf}'])
                # calculate cash dividend on tsNextDay, if any
                try:
                    fltCashDividend = dictOfETFDividends[f'{etf}'].at[tsNextDay, 'Dividend']
                except:
                    fltCashDividend = 0.0
                if fltCashDividend > 0.0:
                    fltCashDividend *= optimizedPortfolio.portfolioAssets.at[tsNextDay, f'{etf}_shares']
                    optimizedPortfolio.portfolioAssets.at[tsNextDay, 'Cash'] += fltCashDividend

            # update the portfolio value
            optimizedPortfolio.portfolio_closing_value(date=tsNextDay, etfs=lstETFs)


        else:
            for etf in lstETFs:
                # update closing price for each etf
                optimizedPortfolio.update_closing_price(date=tsNextDay,
                                                        etf=etf,
                                                        price=dfClosingPriceDataTenYears.at[tsNextDay, f'{etf}'])
            # update the portfolio value
            optimizedPortfolio.portfolio_closing_value(date=tsNextDay, etfs=lstETFs)
    else:
        break

print("Portfolio initial value: $", optimizedPortfolio.portfolioAssets.at[optimizedPortfolio.portfolioAssets.index[0], 'Portfolio Value'])
print("Portfolio end value: $", optimizedPortfolio.portfolioAssets.at[optimizedPortfolio.portfolioAssets.index[-1], 'Portfolio Value'])

dfSPY = Processor.price_data(etfs='SPY', start_date=pd.Timestamp('2014-06-30'), end_date=tsLastTradingDay, OHLCVAC='Adj Close')
dfPercentChange = dfSPY.pct_change()
dfSPYTotalReturns = ((1 + dfPercentChange).cumprod() - 1)

dfOptimizedPortfolioValue = optimizedPortfolio.portfolioAssets['Portfolio Value']
dfPercentChange = dfOptimizedPortfolioValue.pct_change()
dfOptimizedPortfolioReturns = ((1 + dfPercentChange).cumprod() - 1)

plt.plot(dfOptimizedPortfolioReturns, '#18453B')
plt.plot(dfSPYTotalReturns, 'b')
plt.title("Performance of Optimized Portfolio vs. S&P 500 ($SPY)")
plt.ylabel('Cumulative Return')
plt.xlabel('Date')
plt.legend(['Optimized Portfolio', 'S&P 500'], loc='upper left')
plt.show()

path = os.getcwd() + "/Data/Portfolio Data"
optimizedPortfolioDataframe = optimizedPortfolio.portfolioAssets
optimizedPortfolioDataframe.to_csv(os.path.join(path, r'optimizedPortfolio.csv'), na_rep='nan',
                                   date_format='%Y-%m-%d %H:%M:%S')
