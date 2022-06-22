class Portfolio:
    """
    Portfolio Object
    portfolio = {
    "etf ticker 1": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    "etf ticker n": {'rank': int, 'closing price': %.2f, 'opening price': %.2f, '200D MA': %.2f, 'shares': int},
    {'Cash': int}
    }
    """

    # -- Constructor --
    def __init__(self, etfs, portfolioValue):
        # -- Attributes --
        self.__portfolioValue = portfolioValue  # Protected attribute of portfolio value
        self.__portfolioAssets = {'Cash': portfolioValue}  # Initialize portfolio w/ cash
        for i in etfs:  # Initialize portfolio attribute w/ nested dictionary
            self.__portfolioAssets.update({i: {'Rank': int(0),
                                               'Closing price': float(0.00),
                                               'Opening price': float(0.00),
                                               '200D MA': float(0.00),
                                               'Shares': int(0)}})
        print(f"Portfolio instantiated with ${portfolioValue:.2f}\n")

    # -- Properties --
    @property
    def portfolioValue(self):
        return self.__portfolioValue

    @portfolioValue.getter
    def portfolioValue(self):
        """
        :return: Returns float value of portfolio
        """
        for key, info in self.__portfolioAssets.items():
            if key == 'Cash':
                self.__portfolioValue = ([info][0])
            else:
                shares = info['Shares']
                price = info['Closing price']
                x = (shares * price)
                self.__portfolioValue += x
        return self.__portfolioValue

    # -- Methods --
    def reportPortfolioAllocation(self):
        """
        :return: row of key:value of dict info for each ETF
        """
        print("***********************************")
        for key, info in self.__portfolioAssets.items():
            if key == 'Cash':
                print("\nCash: $", ([info][0]), sep="")
            else:
                print("\nETF:", key)
                for i in info:
                    print(i + ':', info[i])
        print("***********************************\n")

    def setPortfolioAsset(self,
                          etf,
                          rank=None,
                          closing_price=None,
                          opening_price=None,
                          MA_200D=None,
                          shares=None):
        if rank is not None:
            self.__portfolioAssets[etf]['Rank'] = rank
        if closing_price is not None:
            self.__portfolioAssets[etf]['Closing price'] = closing_price
        if opening_price is not None:
            self.__portfolioAssets[etf]['Opening price'] = opening_price
        if MA_200D is not None:
            self.__portfolioAssets[etf]['200D MA'] = MA_200D
        if shares is not None:
            self.__portfolioAssets[etf]['Shares'] = shares
        return self.__portfolioAssets

    def getPortfolioAsset(self, etf, item):
        getValue = self.__portfolioAssets[etf][item]
        return getValue

    def setPortfolioCash(self, cash_delta):
        currentCashValue = self.__portfolioAssets.get('Cash')
        setCashValue = cash_delta + currentCashValue
        if setCashValue < 0.00:
            print("Insufficient cash for transaction")
        else:
            self.__portfolioAssets['Cash'] = setCashValue
        return

    def getPortfolioCash(self):
        currentCashValue = self.__portfolioAssets.get('Cash')
        return currentCashValue


# # list of ETFs
# lstETFs = [
#     'MTUM',  # US Stocks Momentum
#     'VTV',  # US Stocks Value
#     'VEU',  # Foreign Developed Stock
#     'VWO',  # Foreign Emerging Stocks
#     'VCIT',  # Corporate Bonds
#     'VGLT',  # 30Y Bonds
#     'BNDX',  # 10Y Foreign BondsPo
#     'VTIP',  # TIPS
#     'DBC',  # Commodities
#     'IAU',  # Gold
#     'VNQ',  # REITS
# ]
#
# # instantiate 2 portfolios
# portfolio1 = Portfolio(lstETFs, 10000.00)
# portfolio2 = Portfolio(lstETFs, 20000.00)
#
# # return portfolio value
# print(f"Portfolio1 value: ${portfolio1.portfolioValue:.2f}")
# print(f"Portfolio2 value: ${portfolio2.portfolioValue:.2f}")
#
# # return portfolio allocation as list of key:value pairs
# portfolio1.reportPortfolioAllocation()
# portfolio2.reportPortfolioAllocation()
#
# # get cash value
# print(f"cash: $", portfolio1.getPortfolioCash(), sep="")
# print(f"cash: $", portfolio2.getPortfolioCash(), sep="")
#
# # set cash value
# portfolio1.setPortfolioCash(cash_delta=+1.00)
# portfolio2.setPortfolioCash(cash_delta=-1.00)
#
# # get cash value
# print(f"cash: $", portfolio1.getPortfolioCash(), sep="")
# print(f"cash: $", portfolio2.getPortfolioCash(), sep="")
#
# # Set asset value
# portfolio1.setPortfolioAsset(etf='VNQ', rank=1, shares=1, closing_price=100.12, MA_200D=101.45)
# portfolio2.setPortfolioAsset(etf='VTV', rank=2, shares=4, closing_price=900.99, MA_200D=893.09)
#
# # get asset value
# print(portfolio1.getPortfolioAsset(etf='VNQ', item='Closing price'))
# print(portfolio2.getPortfolioAsset(etf='VTV', item='200D MA'))
#
# # return portfolio allocation as list of key:value pairs
# portfolio1.reportPortfolioAllocation()
# portfolio2.reportPortfolioAllocation()
#
# # return portfolio value
# print(f"Portfolio1 value: ${portfolio1.portfolioValue:.2f}")
# print(f"Portfolio2 value: ${portfolio2.portfolioValue:.2f}")
