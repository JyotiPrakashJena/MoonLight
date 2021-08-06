import yfinance as yf

from CandleStick import Marubozu

Data = yf.Ticker('PILITA.NS').history(period='1d', interval='15m')
Data.columns = ['open', 'high', 'low', 'close', 'Volume', 'Dividends', 'Stock Splits']

print(Marubozu.detect_pattern(Data))