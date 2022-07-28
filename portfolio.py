import os # remove this
import pandas as pd
from pandas.tseries.offsets import BDay


class Portfolio:
    """
    Portfolio Object - An object that contains a dataframe of cash,
    shares of ETFs, their closing price, and portfolio value, indexed by date

    self.__portfolioAssets : DataFrame =
        Date                Cash       ETF1_shares     ETF1_close   ETFn_shares     ETFn_close      Portfolio Value
        YYYY-MM-DD          float      int             float        int             float           float
    """

    # -- Constructor --
    def __init__(self, etfs, portfolioValue, startDate, data=None):
        # -- Attributes --
        if data is None:
            # startDate -= BDay(1)  # roll back start date 1 day to initialize dataframe
            d = {'Date': [startDate],
                 'Cash': [(float(portfolioValue))]}
            for i in etfs:
                d.update({f'{i}_shares': int(0)})
                d.update({f'{i}_close': float(0.00)})
            d.update({'Portfolio Value': float(portfolioValue)})
            self.__portfolioAssets = pd.DataFrame(data=d).set_index('Date')
            print(f"Portfolio instantiated with ${portfolioValue:.2f}\n")
        else:
            d = data
            self.__portfolioAssets = pd.DataFrame(data=d)
            print(f"Portfolio data loaded")

    # -- Properties --
    @property
    def portfolioAssets(self):
        return self.__portfolioAssets

    # -- Methods --
    def buy_shares_at_open(self, date, etf, shares, cost):
        if cost > self.__portfolioAssets.at[date, 'Cash']:
            print('Insufficient funds')
            self.__portfolioAssets.at[date, f'{etf}_shares'] += shares
            self.__portfolioAssets.at[date, 'Cash'] -= cost
        else:
            self.__portfolioAssets.at[date, f'{etf}_shares'] += shares
            self.__portfolioAssets.at[date, 'Cash'] -= cost

    def sell_shares_at_open(self, date, etf, shares, cost):
        if shares > self.__portfolioAssets.at[date, f'{etf}_shares']:
            print('Insufficient shares')
        else:
            self.__portfolioAssets.at[date, f'{etf}_shares'] -= shares
            self.__portfolioAssets.at[date, 'Cash'] += cost

    def update_closing_price(self, date, etf, price):
        self.__portfolioAssets.at[date, f'{etf}_close'] = price

    def portfolio_closing_value(self, date, etfs):
        cash = self.__portfolioAssets.at[date, 'Cash']
        self.__portfolioAssets.at[date, 'Portfolio Value'] = cash
        for i in etfs:
            shares = self.__portfolioAssets.at[date, f'{i}_shares']
            price = self.__portfolioAssets.at[date, f'{i}_close']
            etfValue = (shares * price)
            self.__portfolioAssets.at[date, 'Portfolio Value'] += etfValue

    def get_portfolio_closing_value(self, date):
        return self.__portfolioAssets.at[date, 'Portfolio Value']

    def add_row_to_dataframe(self, df):
        self.__portfolioAssets = self.__portfolioAssets.append(df, verify_integrity=True)

    def get_last_index(self):
        return self.__portfolioAssets.index[-1]
    # -- End of Class --
