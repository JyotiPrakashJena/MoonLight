from nsetools import Nse
import requests
from SupportResistance import FiboLevels
from prettytable import PrettyTable
import math
import yfinance as yf
from prettytable import PrettyTable

nse = Nse()
Stocks = nse.get_stock_codes()
Stock = dict(list(Stocks.items())[1:])


def message_handler(data, amountPerStock, stock_id, stockName, level):
    t = PrettyTable([stock_id, 'Fibonacci'])
    t.add_row(['Quantity       ', math.ceil(amountPerStock / data['close'][-1])])
    t.add_row(['Buy       ', round(data['close'][-1], 2)])
    t.add_row(['Fibo Value', round(level, 2)])
    return t


def telegram_notification(message):
    response = requests.post("https://api.telegram.org/bot1949861983:AAGcvESU8MIqoXABFXIPt8Ypg5GedRC6P4c/sendMessage",
                             params={'chat_id': '-544542415', 'text': message})


count = 0
for stock_id, stock_name in Stock.items():
    try:
        print(count, end='\r\n')
        data = yf.Ticker(str(stock_id) + '.NS').history(period='1y')
        data.columns = ['open', 'high', 'low', 'close', 'Volume', 'Dividends', 'Stock Splits']
        # data = yf.Ticker(str(stock_id) + '.NS').history(start='2020-07-21', end='2021-07-22')
        Indicator, Level = FiboLevels.fibo_indicator(data)

        count += 1
        if Indicator:
            print(stock_name)
            telegram_notification(message_handler(data, 5000, stock_id, stock_name, Level))
    except Exception as e:
        print(e)
