# Portfolio-Optimization Tool: A quantitative approach to optimal asset allocation

## Preface
- I wanted to learn python, so I decided to build a tool that would help me invest my money in a quantitative, un-biased, and methodical strategy.
- I built this tool without any formal python training. <mark>It is very 'un-pythonic' in its current state. Bare with me as I make updates and improve the tool<mark>.
- I am learning to use Github and Github Pages to build a portfolio of my projects and document how I am learning python and improving the tool.
## Summary
 - This python script was developed to automate the investing strategy of Meb Faber's 'Trinity Portfolio' as described here: [Cambria Investments](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf) (external link)
 - The goal of the Trinity Portfolio is long-term growth, reduced volatility, and to minimize drawdowns 
 - These goals are achieved by building a portfolio that 1) includes all major global asset classes with a tilt towards value, 2) adds a momentum component and 3) employs trend-following
 - The Portfolio Optimization tool uses python and pandas to scrape ETF price data, calculate each ETFs' 200 day moving average and its 1, 3, 6, and 12 month performance
 - This data is concatenated into 3 CSV files, which can be imported to an Excel spreadsheet which will show the user how the portfolio should weight the percent allocation of each asset class for the following month.
 - The tool is run after the close of trading on the last trading day of each month, the new CSVs are added to the spreadsheet, and the allocation for the following month is generated.
 - The portfolio is rebalanced every month.
## Globally-Diversified Investments
The portfolio comprises 11 ETFs which represent all major asset classes.
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
## Timeframes
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

>> 2022-04-23 # Today will return the day the script is run. Ideally this should be run after the close of the last trading day
>> 2022-03-31 00:00:00 # '1 month' in finance days from 4/23 is 3/31, ie the last business day of the prior month
>> 2022-01-31 00:00:00 # '3 months' from 4/23/22 is 1/31/22
>> 2021-10-29 00:00:00 # '6 months' from 4/23/22 is 10/29/22 (10/30/22 and 10/31/22 was Sat and Sun)
>> 2021-04-30 00:00:00 # '1 year' from 4/23 is 4/30/21
```

Now we have the start and end dates for scraping price data and determining ETF returns and calculating the 200 day moving average.

## Using Pandas 
The tool's initial version uses pandas to create dataframes for all the ETFs price data and stores them in memory and timeframes of 1m, 3m, 6m, and 12m from the datetime module.
The
## References
 - Meb Faber (2016). [The Trinity Portfolio](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf)

## To Do
 - add performance and 200 day moving average section
 - add screen captures of spreadsheet

