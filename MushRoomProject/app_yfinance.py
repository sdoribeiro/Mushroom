import yfinance as yf

ITSA4 = yf.Ticker("ITSA4.SA")

print (ITSA4.info['shortName'])
print (ITSA4.info['currentPrice'])