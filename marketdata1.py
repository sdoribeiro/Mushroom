import json
import yfinance as yf
stock_obj = yf.Ticker("PG")
# Here are some fixs on the JSON it returns
validated = str(stock_obj.info).replace("'","\"").replace("None", "\"NULL\"").replace("False", "\"FALSE\"").replace("True", "\"TRUE\"")
# Parsing the JSON here
meta_obj = json.loads(validated)

# Some of the short fields
print("sharesShort: "+str( meta_obj['sharesShort']))
print("shortRatio: "+str( meta_obj['shortRatio']))
print("shortPercentOfFloat: "+str( meta_obj['shortPercentOfFloat']))
print(meta_obj)
