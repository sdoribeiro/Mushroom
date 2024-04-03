import yfinance as yf

GME_data = yf.Ticker("GME")

# get stock info
print(GME_data.info['previousClose'])