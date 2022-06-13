class Portfolio:
    """
    Portfolio Object
    portfolio = {
    "etf ticker 1": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    "etf ticker n": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    {'cash': int}
    }
    """

    # -- Constructor --
    def __init__(self, etfs, portfolioValue):
        # -- Attributes --
        self.__portfolioValue = portfolioValue  # Protected attribute of portfolio value
        self.__portfolio = {'Cash': portfolioValue}  # Initialize portfolio w/ cash
        for i in etfs:  # Initialize portfolio attribute w/ nested dictionary
            self.__portfolio.update({i: {'Rank': int(0),
                                         'Closing price': float(0.00),
                                         'Opening price': float(0.00),
                                         '200D MA': float(0.00),
                                         'Shares': int(0)}})
        print(f"Portfolio instantiated with ${portfolioValue:.2f}")

    # -- Properties --
    @property
    def portfolioValue(self):
        return self.__portfolioValue

    @portfolioValue.getter
    def portfolioValue(self):
        """
        :return: Returns float value of portfolio
        """
        for etf, info in self.__portfolio.items():
            if etf == 'Cash':
                self.__portfolioValue = ([info][0])
            else:
                shares = info['Shares']
                price = info['Closing price']
                x = (shares * price)
                self.__portfolioValue += x
        return self.__portfolioValue

    @property
    def portfolio(self):
        return self.__portfolio

    @portfolio.setter
    def portfolio(self,
                  cash=None,
                  etf=None,
                  rank=None,
                  closing_price=None,
                  opening_price=None,
                  MA_200D=None,
                  shares=None):
        if cash is not None:
            self.__portfolio['Cash'] = cash
        if etf is not None:
            if rank is not None:
                print("set rank")
            if closing_price is not None:
                print("set closing price")
            if opening_price is not None:
                print("set opening price")
            if MA_200D is not None:
                print("set MA_200D")
            if shares is not None:
                print("set shares")

    # -- Methods --
    def reportPortfolioAllocation(self):
        """
        :return: row of key:value of dict info for each ETF
        """
        print("***********************************")
        for etf, info in self.__portfolio.items():
            if etf == 'Cash':
                print("\nCash: $", ([info][0]), sep="")
            else:
                print("\nETF:", etf)
                for key in info:
                    print(key + ':', info[key])
        print("***********************************\n")


# list of ETFs
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
# instantiate 2 portfolios
portfolio1 = Portfolio(lstETFs, 10000.00)
portfolio2 = Portfolio(lstETFs, 20000.00)

# return portfolio value
print(f"Portfolio1 value: ${portfolio1.portfolioValue:.2f}")
print(f"Portfolio2 value: ${portfolio2.portfolioValue:.2f}")

# return portfolio allocation as list of key:value pairs
portfolio1.reportPortfolioAllocation()
portfolio2.reportPortfolioAllocation()

# Set some etf info key/values to a new number
# print(f"Portfolio1 value: ${portfolio1.portfolioValue:.2f}")
# portfolio1.portfolio['VNQ']['Shares'] = 1
# portfolio1.portfolio['VNQ']['Closing price'] = 123.00
# portfolio2.portfolio['VNQ']['Shares'] = 1
# portfolio2.portfolio['VNQ']['Closing price'] = 456.00

# return portfolio value
print(f"Portfolio1 value: ${portfolio1.portfolioValue:.2f}")
print(f"Portfolio2 value: ${portfolio2.portfolioValue:.2f}")
