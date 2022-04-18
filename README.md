# Portfolio-Optimization Tool: A quantitative approach to optimal asset allocation

## Preface
- I wanted to learn python, so I decided to build a tool that would help me invest my money in a quantitative, un-biased, and methodical strategy.
- I built this tool without any formal python training. <mark>It is very 'un-pythonic' in its current state. Bare with me<mark>.
- I am learning to use Github and Github Pages to build a portfolio of my projects and document how I am learning python and improving the tool.
## Summary
 - This python script was developed to automate the investing strategy of Meb Faber's 'Trinity Portfolio' as described here: [Cambria Investments](https://www.cambriainvestments.com/wp-content/uploads/2016/07/Trinity_DIGITAL_final.pdf) (external link)
 - The goal of the Trinity Portfolio is long-term growth, reduced volatility, and to minimize drawdowns 
 - These goals are achieved by building a portfolio that 1) includes all major global asset classes with a tilt towards value, 2) add momentum and 3) add trend-following
 - The Portfolio Optimization tool uses python and pandas to scrape ETF price data, calculate each ETFs' 200 day moving average and its 1, 3, 6, and 12 month performance
 - This data is concatenated into 3 CSV file, which can be imported to an Excel spreadsheet which will show the user how the portfolio should weight the percent allocation of each asset class for the following month.
 - The tool is run after the close of trading on the last trading day of each month, the new CSVs are added to the spreadsheet, and the allocation for the following month is generated.
 - The portfolio is rebalanced every month.
## Globally-Diversified Investments
### Subsection
some python code
```python
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import BDay
from dateutil.relativedelta import *

# Define ETFs in Portfolio
portfolio = [
    'MTUM',  # US Stocks Momentum
    'VTV',  # US Stocks Value
    'VEU',  # Foreign Developed Stock
    'VWO',  # Foreign Emerging Stocks
    'VCIT',  # Corporate Bonds
    'VGLT',  # 30Y Bonds
    'BNDX',  # 10Y Foreign Bonds
    'VTIP',  # TIPS
    'VAW',  # Commodities
    'IAU',  # Gold
    'VNQ',  # REITS
]
```

## To Do
 - write summary and preface
 - clean up path code to save CSVs to current location of python script