import yfinance as yf
import json
import datetime

class Asset:
    def __init__(self, ticker):
        self.ticker = ticker

        # using yfinance to get ticker data
        stock_obj = yf.Ticker(ticker)
        # Here are some fixs on the JSON it returns
        validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
        # Parsing the JSON here
        meta_obj = json.loads(validated)

        self.name = meta_obj['shortName']
        self.price = meta_obj['previousClose']

    def __str__(self):
        return f"{self.ticker},{self.name},{self.price}"

class Reit(Asset):
    pass
   

class Operation:
    def __init__(self, asset, date, quantity, price, tax):
        self.asset = asset
        self.date = date
        self.quantity = quantity
        self.price = price
        self.tax = tax
    def __str__(self):
        return f"{self.asset} | {self.date} | {self.quantity} | {self.price}"

 
class Buy(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = 1.0

     def __str__(self):
        return f"{self.asset} | {self.date} | {self.quantity} | {self.price * self.ope} | {self.tax}"


class Sell(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = -1.0
     def __str__(self):
        return f"{self.asset} | {self.date} | {self.quantity} | {self.price * self.ope} | {self.tax}"


stock1 = Asset('SAPR11.SA')
print ("Asset")
print (stock1)

sapr1 = Buy('SAPR11.SA', datetime.datetime(2021,12,31),300.0, 24.68, 0.0 )
sapr2 = Buy('SAPR11.SA', datetime.datetime(2022,9,28),300.0, 17.12 , 7.14)

mrve1 = Buy('MRVE3.SA', datetime.datetime(2021,1,14),100.0, 20.93 , 0.0)
mrve2 = Buy('MRVE3.SA', datetime.datetime(2021,10,27),100.0, 10.66 , 0.0)
mrve3 = Sell('MRVE3.SA', datetime.datetime(2022,1,21),100.0, 12.09 , 0.0)
mrve4 = Buy('MRVE3.SA', datetime.datetime(2022,3,15),100.00, 9.96 , 0.0)
mrve5 = Sell('MRVE3.SA', datetime.datetime(2022,3,17),100.0, 10.12 , 0.0)


class PortifolioItem(Asset):
    def __init__(self, ticker, perc):
        super().__init__(ticker)
        self.perc = perc

Port1 = PortifolioItem('SAPR11.SA',10.0)
Port2 = PortifolioItem('MRVE3.SA',5.0)
print("Portifolio")
print (Port1.name)
print (Port1.perc)


class PortifolioRef:
    def __init__(self, name):
        self.name = name
        self.assets = []

    def add_ticker(self, ticker):
        self.assets.append(ticker)

pf1 = PortifolioRef('Portifolio Name')
pf1.add_ticker(Port1)
pf1.add_ticker(Port2)
print("Portifolio Ref")
print(pf1.name)
for Asset in pf1.assets:
    print('{} {}'.format(Asset.name, Asset.perc ))



class Carteira:
    def __init__(self, name, asset):
        self.name = name
        self.asset = asset
        self.operations = []
    
    def add_opp(self, operation):
        self.operations.append(operation)


SAPR = Carteira ('Carteira de Acoes', 'SAPR.SA') 
SAPR.add_opp(sapr1)
SAPR.add_opp(sapr2)


MRVE = Carteira ('Carteira de Acoes', 'MRVE.SA')
MRVE.add_opp(mrve1)
MRVE.add_opp(mrve2)
MRVE.add_opp(mrve3)
MRVE.add_opp(mrve4)
MRVE.add_opp(mrve5)

print ('{} {}'.format(SAPR.name, SAPR.asset))

Mprice = 0.0
QtdAsset = 0.0

for Operation in SAPR.operations:
    if Operation.ope > 0:
        if Mprice == 0:
            Mprice = Operation.price
            QtdAsset = Operation.quantity
        else:
            Mprice = round(((Mprice * QtdAsset) + (Operation.price * Operation.quantity))/ (QtdAsset + Operation.quantity),2)
            QtdAsset = QtdAsset + Operation.quantity
    else:
            QtdAsset = QtdAsset - Operation.quantity
    print('{} {} {} {} {} {}'.format(Operation.date, Operation.asset, Operation.quantity, Operation.price , Operation.ope, Mprice))


print (QtdAsset)
print (QtdAsset * Mprice)
# Quantidade total de assets, preco total

Mprice = 0.0
QtdAsset = 0.0

for Operation in MRVE.operations:
    if Operation.ope > 0:
        if Mprice == 0:
            Mprice = Operation.price
            QtdAsset = Operation.quantity
        else:
            Mprice = round(((Mprice * QtdAsset) + (Operation.price * Operation.quantity))/ (QtdAsset + Operation.quantity),2)
            QtdAsset = QtdAsset + Operation.quantity
    else:
            QtdAsset = QtdAsset - Operation.quantity
    print('{} {} {} {} {} {}'.format(Operation.date, Operation.asset, Operation.quantity, Operation.price , Operation.ope, Mprice))


print (QtdAsset)
print (QtdAsset * Mprice)
# Quantidade total de assets, preco total



