# Portfolio-Optimization Tool: A quantitative approach to optimal asset allocation

## Preface
- I wanted to learn python, so I decided to build a tool that would help me invest my money in a quantitative, un-biased, and methodical strategy.
- I built this tool without any formal python training. <mark>It is very 'un-pythonic' in its current state. Bare with me as I make updates and improve the tool<mark>.
- I am learning to use Github and Github Pages to build a portfolio of my projects and document how I am learning python and improving the tool.

## Summary
 - This python script was developed to automate the investing strategy of Meb Faber's 'Trinity Portfolio' as described here: [Cambria Investments](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf) (external link)
 - Faber's Trinity Portfolio has 3  core elements: 1) assets diversified across a global investment set, 2) tilts toward investments exhibiting value and momentum traits, and 3) exposure to trend following.
 - 11 ETFs make up the portfolio (See Listing 1).
 - The first 50% of the portfolio allocates a fixed weighting to each asset class based on Global Market Portfolio (GMP) theory
 - The second 50% uses momentum and trend-following calculations to allocate an additional 10% to the top 5 performing asset classes.
 - Pandas is used to calculate the total return (momentum) and 200 day moving average (trend-following) of each ETF.
 - The script is run once a month after the close of the last trading day and produces 3 .csv files that are imported into a spreadsheet.
 - Formulas in the spreadsheet create the logic that determines the total allocation of all asset classes for the portfolio for the following month.
---
# Version 1.0.: Portfolio Optimization Tool
## 1st 50%: 'Buy and hold' fixed weighting
The portfolio comprises 11 ETFs which represent all major asset classes. The strategy tries to get the 'best of both worlds' by making 50% of the portfolio 'buy and hold'
and the other 50% be dynamically allocated based on momentum and trend-following. Below is the fixed weighting based on GMP theory.
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
    'VAW',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]
``` 
Listing 1. List of ETF symbol names

## 2nd 50%: Momentum and Trend-Following
The tool uses Pandas to calculate total return and 200 day simple moving averages (200DSMA) of all asset classes.
Below is rough pseudo-code that describes the method for determining the momentum and trend-following allocation.
```
for etf in portfolio:
    calculate etf 1,3,6,12 month total return
    average etf 1,3,6,12 month total return
    rank etf average return (1st{best} - 11th{worst})
    use pandas to calculate etf 200DSMA
    use pandas to find etf closing price on last trading day of month
    if etf closing price > 200DSMA and etf average return rank < 6:
        allocate extra 10% to etf

if 5 etfs dont satisfy the logical expression, allocte any remaining portion to cash
ie. if only 4 etfs rank in the top 5 and are above 200DSMA, allocate 10% cash
    if only 2 etfs rank in the top 5 and are above 200DSMA, allocate 30% cash
    if 0 etfs rank in the top 5 and are above 200DSMA, allocate 50% cash
```
Listing 2. Pseudo-code for momentum and trend-following with logic checks

Now that the method for allocating the 2nd 50% (5 x 10% for the top 5 etfs, or a remainder in cash)
lets look at how the tool performs these steps.

### Timeframes for total returns
The tool follows Faber's strategy by creating timeframes for calculating returns of each ETFs. These variables store start and end dates that are used as parameters for calculating returns and  200 day moving averages.
Investment returns are calculated by finding the change in price from the last business day of each month, ie the total 1 month return from 4/29/22 (the last trading day in April 2022) is calculated from 3/31/22 (the last trading day in March).
Each timeframe works by finding the first day of the current month. Then it will subtract the number of months for each time frame, then subtract a final business day BDay() to return the last trading day of the timeframe.
```python
# Define time frames
today = dt.date.today()
one_month = dt.date(today.year, today.month, 1) - relativedelta(months=0, days=0) - BDay()
three_month = dt.date(today.year, today.month, 1) - relativedelta(months=2, days=0) - BDay()
six_month = dt.date(today.year, today.month, 1) - relativedelta(months=5, days=0) - BDay()
one_year = dt.date(today.year, today.month, 1) - relativedelta(months=11, days=0) - BDay()
print(today, one_month, three_month, six_month, one_year, sep="\n")

>> 2022-04-29 # Today will return the day the script is run. This should be run after the close of the last trading day
>> 2022-03-31 00:00:00 # '1 month' in finance days from 4/29/22 is 3/31/22, ie the last business day of the prior month
>> 2022-01-31 00:00:00 # '3 months' from 4/29/22 is 1/31/22
>> 2021-10-29 00:00:00 # '6 months' from 4/29/22 is 10/29/22 (10/30/22 and 10/31/22 was Sat and Sun)
>> 2021-04-30 00:00:00 # '1 year' from 4/29/22 is 4/30/21
```

Now we have the start and end dates for scraping price data and determining ETF returns and calculating the 200 day moving average.

### Using Pandas 
The tool's initial version uses pandas to create dataframes for all the ETFs price data and stores them in memory and timeframes of 1m, 3m, 6m, and 12m from the datetime module.
This is not the best way to do this (ie. without using functions and objects) but later versions will correct this and handle more 
of the methodology entirely in python as etf objects, vs dataframes like in R programming.

The `pandas` library and `pandas_datareader.data` as `web` give the tool functionality to retrieve stock/etf price data and save dataframes
of 1,3,6,12 months using the following code. `ETF_price_data_latest = ETF_price_data_one_year.tail(1)` returns the closing price.
```python
# Create 1m, 3m, 6m, & 1y data frames of daily closing price for all ETFs
ETF_price_data_one_month = web.DataReader(portfolio, 'yahoo', one_month, today)['Adj Close']
ETF_price_data_three_month = web.DataReader(portfolio, 'yahoo', three_month, today)['Adj Close']
ETF_price_data_six_month = web.DataReader(portfolio, 'yahoo', six_month, today)['Adj Close']
ETF_price_data_one_year = web.DataReader(portfolio, 'yahoo', one_year, today)['Adj Close']
ETF_price_data_latest = ETF_price_data_one_year.tail(1)
```

### Total Returns
Now that we have dataframes of price data, we can calculate the total return 
for each timeframe then concatenate the results using `pd.concate` to a list of returns.
The .tail(1) returns the return on the last day of the timeframe, which is the only one we care about. 
```python
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
```

### 200DSMA
The 1 year time frame must be used (for obvious reasons) to calculate the 200DSMA. The `.rolling`
function gives us our window parameter and the `.mean()` function averages over the
window. Again, `.tail()` returns only the last day's 200DSMA so we can compare against the closing price on the last trading
day of the month. 
```python
# Create data frames of 200 day simple moving average
ETF_price_data_one_year_close = web.DataReader(portfolio, 'yahoo', one_year, today)['Close']
ETF_price_data_200D_SMA = ETF_price_data_one_year_close.rolling(window=200).mean()
ETF_price_data_200D_SMA_latest = ETF_price_data_200D_SMA.tail(1)
```
### Export dataframes as CSVs
The current working directory is found and all the dataframes are exported to csv files in /CSV.
These CSVs are copied into the spreadsheet and the functions within tabulate the trend-following portion
that to the buy and hold portion.
```python
# Create CSV for closing price data, 200 day simple moving average data, and returns data
path = os.getcwd() + "/CSVs"
ETF_price_data_one_year.to_csv(os.path.join(path, r'Portfolio 1 Year Closing Price Data.csv'))
ETF_price_data_200D_SMA_latest.to_csv(os.path.join(path, r'Portfolio Latest 200D SMA.csv'))
Portfolio_returns.to_csv(os.path.join(path, r'Portfolio Returns.csv'))
```
### Final Output
The tool was ran on 3-31-22 and the formulas in the spreadsheet implement the logic
described in the pseudo-code above. This would give the user the percent allocation his or her
portfolio should have for teh following month, 4/22.

![portfolio 3-31-22](docs/portfolio-3-31-22.png?raw=true)
Figure 2. Output in excel showing allocation for the month of 4/22

### References
 - Meb Faber (2016). [The Trinity Portfolio](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf)

### To Do
- convert .ods spreadsheet to .xlsx
- add some error handling for the /CSVs folder to just create one if not found
- automatically export CSVs to .xlsx (.ods is not support in `.to_csv`)
- I would like this to be a jupyter notebook or a living github page. I want main.py to run on the backend once per month and just auto update weightings in the portfolio
- I also want to build a backtester since this can only run in the current month

