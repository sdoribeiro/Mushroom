import yfinance as yf
import json

class Asset:
    def __init__(self, id):
        self.id = id
        stock_obj = yf.Ticker(id)
        # Here are some fixs on the JSON it returns
        validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
        # Parsing the JSON here
        meta_obj = json.loads(validated)
        self.name = meta_obj['shortName']
        self.price = meta_obj['previousClose']

class Reit(Asset):
    pass

class Portifolio(Asset):
    def __init__(self, id, perc):
        super().__init__(id)
        self.perc = perc

class Operation:
    def __init__(self, asset, date, quantity, price):
        self.asset = asset
        self.date = date
        self.quantity = quantity
        self.price = price

class Buy(Operation):
    pass

class Sell(Operation):
    pass

class PortifolioRef:
    def __init__(self, name):
        self.name = name
        self.assets = []

    def add_ticker(self, ticker):
        self.assets.append(ticker)


stock1 = Asset('SAPR11.SA')
stock2 = Asset('ITSA4.SA')
stock3 = Asset('MRVE3.SA')

reit1 = Reit('HGLG11.SA')
reit2 = Reit('IRDM11.SA')
reit3 = Reit('KNRI11.SA')

print ('{} {}'.format(stock1.id, stock1.price))
print ('{} {}'.format(stock2.id, stock2.price))
print ('{} {}'.format(stock3.id, stock3.price))

print ('{} {}'.format(reit1.id, reit1.price))
print ('{} {}'.format(reit2.id, reit2.price))
print ('{} {}'.format(reit3.id, reit3.price))



Port1 = Portifolio('SAPR11.SA',10.0)

Port2 = Portifolio('ITSA4.SA',25.0)
print (Port1.name)
print (Port1.perc)


pf1 = PortifolioRef('teste1')
pf1.add_ticker(Port1)
pf1.add_ticker(Port2)
print(pf1.name)
print(pf1.assets)

for Asset in pf1.assets:
    print('{} {}'.format(Asset.name, Asset.perc ))


#portifolioRef = [Asset('SAPR11.SA', 10.0), Asset('ITSA4.SA', 10.0), Asset('MRVE3.SA',10.0), Reit('HGLG11.SA', 10.0), Reit('IRDM11.SA', 10.0)]

# print all assets linked with one portifolio
#for Asset in portifolioRef:
#    print ('{} {}'.format(Asset.name, Asset.perc))

# Operacao Asset, data, operacao, quantidade, valor unit

