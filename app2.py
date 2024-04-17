import yfinance as yf
import json
import datetime

class Asset:
    def __init__(self, ticker, perc):
        self.ticker = ticker
        self.perc = perc

        # using yfinance to get ticker data
        stock_obj = yf.Ticker(ticker)
        # Here are some fixs on the JSON it returns
        validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
        # Parsing the JSON here
        meta_obj = json.loads(validated)

        self.name = meta_obj['shortName']
        self.price = meta_obj['previousClose']

    def __str__(self):
        return f"{self.ticker},{self.name},{self.price},{self.perc}"

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

SAPR = Asset('SAPR11.SA',10)
MRVE = Asset('MRVE3.SA',5)
print ("Asset")
print (SAPR)
print(MRVE)

# Conjunto de Operacoes SAPR11
sapr1 = Buy('SAPR11.SA', datetime.datetime(2021,12,31),300.0, 24.68, 0.0 )
sapr2 = Buy('SAPR11.SA', datetime.datetime(2022,9,28),300.0, 17.12 , 7.14)
# Conjunto de Operacoes MRVE3
mrve1 = Buy('MRVE3.SA', datetime.datetime(2021,1,14),100.0, 20.93 , 0.0)
mrve2 = Buy('MRVE3.SA', datetime.datetime(2021,10,27),100.0, 10.66 , 0.0)
mrve3 = Sell('MRVE3.SA', datetime.datetime(2022,1,21),100.0, 12.09 , 0.0)
mrve4 = Buy('MRVE3.SA', datetime.datetime(2022,3,15),100.00, 9.96 , 0.0)
mrve5 = Sell('MRVE3.SA', datetime.datetime(2022,3,17),100.0, 10.12 , 0.0)

class Carteira:
    def __init__(self, name, asset):
        self.name = name
        self.asset = asset
        self.operations = []
        self.Mprice = 0
        self.QtdAsset = 0
      
    def add_opp(self, operation):
        self.operations.append(operation)
        if operation.ope > 0: # buy
           if self.Mprice == 0:
              self.Mprice = operation.price
              self.QtdAsset = operation.quantity
           else:  #sell
               self.Mprice = round(((self.Mprice * self.QtdAsset) + (operation.price * operation.quantity))/ (self.QtdAsset + operation.quantity),2)
               self.QtdAsset = self.QtdAsset + operation.quantity
        else:
            self.QtdAsset = self.QtdAsset - operation.quantity

SAPR = Carteira ('Carteira de Acoes', 'SAPR.SA') 
SAPR.add_opp(sapr1)
print ('{} {}'.format(SAPR.name, SAPR.asset))
print ('{}'.format( SAPR.Mprice))
print ('{}'.format(SAPR.QtdAsset))

SAPR.add_opp(sapr2)

print ('{} {}'.format(SAPR.name, SAPR.asset))
print ('{}'.format( SAPR.Mprice))
print ('{}'.format(SAPR.QtdAsset))

for opts in SAPR.operations:
    print ('{}, {}, {}, {}, {}'.format(opts.ope, opts.asset, opts.date, opts.quantity, opts.price))








