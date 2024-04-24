import yfinance as yf
import json
import datetime

# Automacao da gestao de uma carteira de investimentos com base nos percentuais de alocacao pre estabelecidos
# e ativos selecionados.

class Asset:
    def __init__(self, ticker, perc):
        self.ticker = ticker
        # using yfinance to get ticker data
        stock_obj = yf.Ticker(ticker)
        # Here are some fixs on the JSON it returns
        validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
        # Parsing the JSON here
        meta_obj = json.loads(validated)
        self.name = meta_obj['shortName']
        self.name = ticker
       
        self.price = meta_obj['previousClose']
        # adding fields Carteira
        self.operations = []
        self.Mprice = 0
        self.QtdAsset = 0
        self.perc = perc

    def add_opp(self, operation):
        self.operations.append(operation)
        if operation.ope > 0: # buy
           # Calc average price
           if self.Mprice == 0:
              self.Mprice = operation.price
              self.QtdAsset = operation.quantity
           else:  #sell
               self.Mprice = round(((self.Mprice * self.QtdAsset) + (operation.price * operation.quantity))/ (self.QtdAsset + operation.quantity),2)
               self.QtdAsset = self.QtdAsset + operation.quantity
        else:
            self.QtdAsset = self.QtdAsset - operation.quantity

    def __str__(self):
        return f"Asset class: Ticker {self.ticker} | Name {self.name} | Price: {self.price} | Perc: {self.perc} | Mprice: {self.Mprice} | QtdAsset: {self.QtdAsset}"
  
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
        return f"Operation class: Asset {self.asset} | Date {self.date} | Qtd {self.quantity} | Price {self.price} | {self.tax}"

class Buy(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = 1.0

     def __str__(self):
        return f"Buy operation: Asset {self.asset} | Date {self.date} | Qtd {self.quantity} | Price {self.price * self.ope} | {self.tax}"

class Sell(Operation): 
     def __init__(self, asset, date, quantity, price, tax):
        super().__init__(asset, date, quantity, price, tax)
        self.ope = -1.0
     def __str__(self):
        return f"Sell Operation: Asset {self.asset} | Date {self.date} | Qtd {self.quantity} | Price  {self.price * self.ope} | {self.tax}"


print("### 1 ### Criacao Assets")
SAPR = Asset('SAPR11.SA', 90.0)
MRVE = Asset('MRVE3.SA', 10.0)
ITSA = Asset('ITSA4.SA', 10)
ABEV = Asset('ABEV3.SA', 10.0)

print(SAPR)
print(MRVE)
print(ITSA)
print(ABEV)


# Conjunto de Operacoes SAPR11
sapr1 = Buy('SAPR11.SA', datetime.datetime(2021,12,31),300.0, 24.68, 0.0 )
sapr2 = Buy('SAPR11.SA', datetime.datetime(2022,9,28),300.0, 17.12 , 7.14)
# Conjunto de Operacoes MRVE3
mrve1 = Buy('MRVE3.SA', datetime.datetime(2021,1,14),100.0, 20.93 , 0.0)
mrve2 = Buy('MRVE3.SA', datetime.datetime(2021,10,27),100.0, 10.66 , 0.0)
mrve3 = Sell('MRVE3.SA', datetime.datetime(2022,1,21),100.0, 12.09 , 0.0)
mrve4 = Buy('MRVE3.SA', datetime.datetime(2022,3,15),100.00, 9.96 , 0.0)
mrve5 = Sell('MRVE3.SA', datetime.datetime(2022,3,17),100.0, 10.12 , 0.0)
# Conjunto de Operacoes ITSA4
itsa1 = Buy('ITSA4.SA', datetime.datetime(2022,5,4),500,8.90,6.91)
itsa2 = Buy('ITSA4.SA', datetime.datetime(2022,11,11),50,13.65,0.0)
itsa3 = Buy('ITSA4.SA', datetime.datetime(2023,9,22),7,6.50,0.0)
itsa4 = Buy('ITSA4.SA', datetime.datetime(2023,10,30),27,17.92,0.0)
# Conjunto de Operacoes ABEV3
#abev1 = Buy('ABEV3.SA', datetime.datetime(2022,5,18),500,17.92,0.0)

print("### 2 ### Inclusao de Operacoes")

# Adiciona operacoes SAPR
SAPR.add_opp(sapr1)
SAPR.add_opp(sapr2)

# Adiciona operacoes MRVE
MRVE.add_opp(mrve1)
MRVE.add_opp(mrve2)
MRVE.add_opp(mrve3)
MRVE.add_opp(mrve4)
MRVE.add_opp(mrve5)

# Adiciona Operacoes ITSA4
ITSA.add_opp(itsa1)
ITSA.add_opp(itsa2)
ITSA.add_opp(itsa3)
ITSA.add_opp(itsa4)

# Adiciona Operacoes ABEV

print("# Exibe situacao ativos")

print(SAPR)
print(MRVE)
print(ITSA)

### CALCULO DA CARTEIRA REAL ###

class Portifolio:
    def __init__(self,name):
        self.name = name
        self.composicao = {}
        self.vlrTotal = 0 

    def add_asset(self, asset):
        self.composicao[asset.ticker+"%REF"] = asset.perc
        self.composicao[asset.ticker] = (asset.price * asset.QtdAsset)
        self.vlrTotal = self.vlrTotal + (asset.price * asset.QtdAsset)
 
    # selecionar somente as chaves que referencia o asset padrao.
    def calc_perc(self):
        aux = {}
        for x in self.composicao.keys():
            a = x[len(x)-2:len(x)]
            if x[len(x)-2:len(x)] == "SA":
                y = x[0:len(x)]+"_%"
                aux[y]=round(self.composicao[x]/self.vlrTotal,2)*100

        for x in aux.keys():
            self.composicao[x]=aux[x]

    def __str__(self):
        return f"Class Portifolio: {self.name} | {self.vlrTotal} | {self.composicao}"


print("### 3 ### - Composicao Portifolio Preco Atual")
MinhaCarteira = Portifolio("Minha Carteira")
MinhaCarteira.add_asset(SAPR)
MinhaCarteira.add_asset(MRVE)
MinhaCarteira.add_asset(ITSA)

print(MinhaCarteira)

# funcao para calcular percentual de cada ativo em relacao ao patrimonio total

MinhaCarteira.calc_perc()
print("### 4 ### Carteira apos apuracao do percentual vs patrimonio total ")
print(MinhaCarteira)

