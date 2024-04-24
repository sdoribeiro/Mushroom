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
        return f"Asset class: {self.ticker} | {self.name} | {self.price} | {self.perc}"

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
        return f"Operation class: {self.asset} | {self.date} | {self.quantity} | {self.price} | {self.tax}"

class Buy(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = 1.0

     def __str__(self):
        return f"Buy operation: {self.asset} | {self.date} | {self.quantity} | {self.price * self.ope} | {self.tax}"

class Sell(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = -1.0
     def __str__(self):
        return f"Sell Operation: {self.asset} | {self.date} | {self.quantity} | {self.price * self.ope} | {self.tax}"

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

    def __str__(self):
        return f"Class Carteira: {self.name} | {self.asset} | {self.Mprice} | {self.QtdAsset})"

print("#### 1 ####")
SAPR = Asset('SAPR11.SA',10.00)
print(SAPR)
MRVE = Asset('MRVE3.SA',5.00)
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

stock1 = Carteira ('Posicao em SAPR', 'SAPR.SA') 
print("#### 2 ####")
print(stock1)
# Adiciona operacoes SAPR

stock1.add_opp(sapr1)
stock1.add_opp(sapr2)

for opts in stock1.operations:
    print ('{}, {}, {}, {}, {}'.format(opts.ope, opts.asset, opts.date, opts.quantity, opts.price))
print(stock1)

print("#### 3 ####")

stock2 = Carteira ('Posicao em  MRVE', 'MRVE3.SA')
print(stock2)
# Adiciona operacoes MRVE

stock2.add_opp(mrve1)
stock2.add_opp(mrve2)
stock2.add_opp(mrve3)
stock2.add_opp(mrve4)
stock2.add_opp(mrve5)
for opts in stock2.operations:
    print ('{}, {}, {}, {}, {}'.format(opts.ope, opts.asset, opts.date, opts.quantity, opts.price))

print (stock2)


### CALCULO DA CARTEIRA REAL ###

class CarteiraReal:
    def __init__(self,name):
        self.name = name
        self.composicao = {}
        self.vlrTotal = 0

    def add_asset(self, asset):
        self.composicao[asset.asset+"_$"] = (asset.Mprice * asset.QtdAsset)
        self.vlrTotal = self.vlrTotal + (asset.Mprice * asset.QtdAsset)
    
    def calc_perc(self):
        aux = {}
        for x in self.composicao.keys():
            y = x[0:len(x)-1]+"%"
            aux[y]=self.composicao[x]/self.vlrTotal

        for x in aux.keys():
            self.composicao[x]=aux[x]

    def __str__(self):
        return f"Class CarteiraReal: {self.name} | {self.vlrTotal} | {self.composicao}"


CR = CarteiraReal("Carteira Real")
CR.add_asset(stock2)
print(CR)
CR.add_asset(stock1)
print(CR)
CR.calc_perc()

print(CR)



    

