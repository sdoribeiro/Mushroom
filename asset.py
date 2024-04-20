import yfinance as yf
import json

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
        return f"{self.ticker} | {self.name} | {self.price} | {self.perc}"

class Reit(Asset):
    pass

SAPR = Asset('SAPR11.SA',10.00)
MRVE = Asset('MRVE3.SA',5.00)

print ("Carteira Referencia")
print (SAPR)
print(MRVE)