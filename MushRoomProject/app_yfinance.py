import yfinance as yf

ITSA4 = yf.Ticker("ITSA4.SA")
print (ITSA4.info['ticker'])
print (ITSA4.info['name'])
print (ITSA4.info['currentPrice'])