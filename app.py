import yfinance as yf

import json

class Asset:
    def __init__(self, id):
        self.id = id
        stock_obj = yf.Ticker(self.id)
        # Here are some fixs on the JSON it returns
        validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
        # Parsing the JSON here
        meta_obj = json.loads(validated)
        self.name = meta_obj['shortName']
        self.price = meta_obj['previousClose']

class Reit(Asset):
    pass

stock1 = Asset('SAPR11.SA')
stock2 = Asset('ITSA4.SA')
stock3 = Asset('MRVE3.SA')

reit1 = Reit('HGLG11.SA')
reit2 = Reit('IRDM11.SA')
reit3 = Reit('KNRI11.SA')


print ('{} {}'.format(stock1.name, stock1.price))
print ('{} {}'.format(stock2.name, stock2.price))
print ('{} {}'.format(stock3.name, stock3.price))

print ('{} {}'.format(reit1.name, reit1.price))
print ('{} {}'.format(reit2.name, reit2.price))
print ('{} {}'.format(reit3.name, reit3.price))


