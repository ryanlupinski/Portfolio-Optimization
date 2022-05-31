class Portfolio:
    """
    Portfolio Object

    portfolio = {
    "etf ticker 1": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    "etf ticker n": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    {'cash': int} <-- RAL: not sure how to handle cash omitting for now
    }
    """

    # -- Fields --
    # -- Constructor --
    def __init__(self, etfs, portfolioValue):
        # -- Attributes --
        self.portfolio = {'cash': portfolioValue}  # Initialize portfolio w/ cash
        self.__portfolioValue = portfolioValue  # Protected attribute of portfolio value
        for i in etfs:  # Initialize portfolio attribute w/ nested dictionary
            self.portfolio.update({i: {'Rank': 0, 'Closing price': 0, 'Opening price': 0, '200D MA': 0, 'Shares': 0}})
        print(f"Portfolio instantiated with ${portfolioValue:.2f}")

    # -- Properties --
    @property
    def portfolioValue(self):
        return self.__portfolioValue

    # -- Methods --


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
portfolio = Portfolio(lstETFs, 10000.00)

# portfolio.portfolio['VNQ']['rank'] = 19
# portfolio.portfolio['VNQ']['closing price'] = 100

for etf, info in portfolio.portfolio.items():
    if etf == 'cash':
        print("\nCash: $", ([info][0]), sep="")
    else:
        print("\nETF:", etf)
        for key in info:
            print(key + ':', info[key])

for etf, info in portfolio.portfolio.items():
    if etf == 'cash':
        value = ([info][0])
    else:
        shares = info['Shares']
        price = info['Closing price']
        x = shares * price
        value += x
print(f"\nPortfolio Value: ${value:.2f}")
