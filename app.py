import yfinance as yf
import json
import datetime

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
        self.price = meta_obj['previousClose']
        self.perc = perc
    def __str__(self):
        return f"{self.ticker},{self.name},{self.price},{self.perc}"

class Reit(Asset):
    pass

ABEV = Asset('ITSA4.SA',10.0)

print(ABEV)

