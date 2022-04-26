# Portfolio-Optimization Tool: A quantitative approach to optimal asset allocation

## Preface
- I wanted to learn python, so I decided to build a tool that would help me invest my money in a quantitative, un-biased, and methodical strategy.
- I built this tool without any formal python training. <mark>It is very 'un-pythonic' in its current state. Bare with me as I make updates and improve the tool<mark>.
- I am learning to use Github and Github Pages to build a portfolio of my projects and document how I am learning python and improving the tool.
## Summary
 - This python script was developed to automate the investing strategy of Meb Faber's 'Trinity Portfolio' as described here: [Cambria Investments](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf) (external link)
 - Faber's Trinity Portfolio has 3  core elements: 1) assets diversified across a global investment set, 2) tilts toward investments exhibiting value and momentum traits, and 3) exposure to trend following.
 - 11 ETFs make up the portfolio (See Listing 1).
 - The first 50% of the portfolio allocates a fixed weighting to each asset class based on Global Market Portfolio theory
 - The second 50% uses momentum and trend-following calculations to allocate an additional 10% to the top 5 performing asset classes.
 - Pandas is used to calculate the total return (momentum) and 200 day moving average (trend-following) of each ETF.
 - The script is run once a month after the close of the last trading day and produces 3 .csv files that are imported into a spreadsheet.
 - Formulas in the spreadsheet create the logic that determines the total allocation of all asset classes for the portfolio for the following month.
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
Listing 1
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

