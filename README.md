# Portfolio-Optimization Tool: A quantitative approach to optimal asset allocation
## Summary
 - This python script was developed to automate the investing strategy of Meb Faber's 'Trinity Portfolio' as described here: [Cambria Investments](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf) (external link)
 - Faber's Trinity Portfolio has 3  core elements: 1) assets diversified across a global investment set 2) tilts toward value and momentum and 3) exposure to trend following.
 - 11 ETFs make up the portfolio (See Listing 1).
 - The first 50% of the portfolio allocates a fixed weighting to each asset class based on Global Market Portfolio (GMP) theory
 - The second 50% uses momentum and trend-following calculations to allocate an additional 10% to the top 5 performing asset classes.
 - Pandas is used to calculate the total return (momentum) and 200 day moving average (trend-following) of each ETF.
 - The script is run once a month after the close of the last trading day and produces 3 .csv files that are imported into a spreadsheet.
 - Formulas in the spreadsheet create the logic that determines the total allocation of all asset classes for the portfolio for the following month.
---
# Version 2.0.: Portfolio Optimization Tool
## 1st 50%: 'Buy and hold' fixed weighting
The portfolio comprises 11 ETFs which represent all major asset classes. The strategy tries to get the 'best of both worlds' by making 50% of the portfolio 'buy and hold'
and the other 50% be dynamically allocated based on momentum and trend-following. Below is the fixed weighting based on GMP theory. We will divide each percentage listed below by 2 and use that as our 'buy and hold' portion.
![Fixed weight](docs/GMP-fixed-weight.png?raw=true)

Figure 1. Fixed weight allocation portion of portfolio

```python
# Define ETFs in Portfolio
portfolio = [
    'MTUM', # US Stocks Momentum
    'VTV',  # US Stocks Value
    'VEU',  # Foreign Developed Stock
    'VWO',  # Foreign Emerging Stocks
    'VCIT', # Corporate Bonds
    'VGLT', # 30Y Bonds
    'BNDX', # 10Y Foreign Bonds
    'VTIP', # TIPS
    'DBC',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]
``` 
Listing 1. List of ETF symbol names

## 2nd 50%: Momentum and Trend-Following
The tool uses Pandas to calculate total return and 200 day simple moving averages (200-Day SMA) of all asset classes.
Below is rough pseudocode that describes the method for determining the momentum and trend-following allocation.
```
for etf in portfolio:
    calculate etf 1,3,6,12 month total return
    average etf 1,3,6,12 month total return
    rank etf average return (1st{best} - 11th{worst})
    use pandas to calculate etf 200DSMA
    use pandas to find etf closing price on last trading day of month
    if etf closing price > 200DSMA and etf average return rank < 6:
        allocate extra 10% to etf

if 5 etfs dont satisfy the previous if statement, allocte any remaining portion to cash
ie. if only 4 etfs rank in the top 5 and are above 200DSMA, allocate remaining 10% cash
    if only 2 etfs rank in the top 5 and are above 200DSMA, allocate remaining 30% cash
    if 0 etfs rank in the top 5 and are above 200DSMA, allocate 50% cash
```
Listing 2. Pseudocode for momentum and trend-following with logic checks

Now that the method for allocating the 2nd 50% (5 x 10% for the top 5 etfs, or a remainder in cash)
lets look at how the tool performs these steps.

### Timeframes for total returns
The tool follows Faber's strategy by creating timeframes for calculating returns of each ETF. These variables store start and end dates that are used as parameters for calculating returns and  200 day moving averages.
Investment returns are calculated by finding the change in price from the last business day of each month, ie the total 1-month return from 4/29/22 (the last trading day in April 2022) is calculated from 3/31/22 (the last trading day in March).
Each timeframe works by finding the first day of the current month. Then it will subtract the number of months for each time frame, then subtract a final business day BDay() to return the last trading day of the timeframe.
```python
# Define time frames
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
        today = dt.date.today()
        dateReturn = dt.datetime(today.year, today.month, 1) - relativedelta(years=years, months=months) - BDay()
        return dateReturn
```
```python
lastTradingDayOfMonth = Processor.time_frame(years=0, months=0)
oneMonth = Processor.time_frame(years=0, months=1)
threeMonths = Processor.time_frame(years=0, months=3)
sixMonths = Processor.time_frame(years=0, months=6)
oneYear = Processor.time_frame(years=1, months=0)

>> 2022-04-29 00:00:00 # lastTradingDayOfMonth will return the last trading day of the month
>> 2022-03-31 00:00:00 # '1 month' in finance days from 4/29/22 is 3/31/22, ie the last business day of the prior month
>> 2022-01-31 00:00:00 # '3 months' from 4/29/22 is 1/31/22
>> 2021-10-29 00:00:00 # '6 months' from 4/29/22 is 10/29/22 (10/30/22 and 10/31/22 was Sat and Sun)
>> 2021-04-30 00:00:00 # '1 year' from 4/29/22 is 4/30/21
```

Now we have the start and end dates for scraping price data and determining ETF returns and calculating the 200-day moving average.

### Using Pandas 
The tool's initial version uses pandas to create dataframes for all the ETFs price data and stores them in memory and timeframes of 1m, 3m, 6m, and 12m from the datetime module.
This is not the best way to do this (i.e. without using functions and objects) but later versions will correct this and handle more 
of the methodology entirely in python as etf objects, vs dataframes like in R programming.

The `pandas` library and `pandas_datareader.data` as `web` give the tool functionality to retrieve stock/etf price data and save dataframes
of 1,3,6,12 months using the following code. `dfETFPriceDataLatest = dfETFPriceDataOneYear.tail(1)` returns the closing price.
```python
class Processor:    
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

# Create 1m, 3m, 6m, & 1y data frames of daily closing price for all ETFs in portfolio
dfETFPriceDataOneMonth = Processor.price_data(etfs=lstETFs, time_frame=oneMonth)
dfETFPriceDataThreeMonth = Processor.price_data(etfs=lstETFs, time_frame=threeMonths)
dfETFPriceDataSixMonth = Processor.price_data(etfs=lstETFs, time_frame=sixMonths)
dfETFPriceDataOneYear = Processor.price_data(etfs=lstETFs, time_frame=oneYear)
dfETFPriceDataLatest = dfETFPriceDataOneYear.tail(1)
```

### Total Returns
Now that we have dataframes of price data, we can calculate the total return 
for each timeframe then concatenate the results using `pd.concate` to a list of returns.
The .tail(1) returns the return on the last day of the timeframe, which is the only one we care about. 
```python
class Processor:   
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
```

### 200-Day Simple Moving Average
The 1-year time frame must be used (for obvious reasons) to calculate the 200-Day SMA. The `.rolling`
function gives us our window parameter and the `.mean()` function averages over the
window. Again, `.tail()` returns only the last day's 200-Day SMA, so we can compare against the closing price on the last trading
day of the month. 
```python
class Processor: 
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
# Create dataframes of 200 day simple moving average for all ETFs in portfolio
dfETF200DayMovingAverage = Processor.moving_average(etfs=lstETFs, time_frame=oneYear)
dfETF200DayMovingAverageLatest = dfETF200DayMovingAverage.tail(1)
```
### Export dataframes as CSVs
The current working directory is found and all the dataframes are exported to csv files in /CSV.
These CSVs are copied into the spreadsheet and the functions within tabulate the trend-following portion
that to the buy and hold portion.
```python
# Create csvs for closing price data, 200 day simple moving average data, and returns data
path = os.getcwd() + "/CSVs"
dfETFPriceDataOneYear.to_csv(os.path.join(path, r'Portfolio 1 Year Closing Price Data.csv'))
dfETF200DayMovingAverageLatest.to_csv(os.path.join(path, r'Portfolio Latest 200D SMA.csv'))
dfTotalReturns.to_csv(os.path.join(path, r'Portfolio Returns.csv'))
```
### Final Output
The tool was run on 4-30-22 and the formulas in the spreadsheet implement the logic
described in the pseudocode above. This would give the user the percent allocation his or her
portfolio should have for the following month, 5/22.

![portfolio 4-30-22](docs/portfolio-4-30-22.png?raw=true)
Figure 2. Output in Excel showing allocation for the month of 5/22

### References
 - Meb Faber (2016). [The Trinity Portfolio](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf)
