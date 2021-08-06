import requests
from nsetools import Nse
import yfinance as yf
from CandleStick import brain_candle
from Volume import volume_indicator
from Indicator import technical_indicator
from SupportResistance import sr_indicator
from Performance import handler
import pandas as pd
from prettytable import PrettyTable
import math
import datetime
import pytz

nse = Nse()
Stocks = nse.get_stock_codes()
Stock = dict(list(Stocks.items())[1:])
candle_stick = 0
count = 0
amountPerStock = 5000


def get_filenames():
    IST = pytz.timezone('Asia/Kolkata')
    ist_today = datetime.datetime.now(IST)
    ist_prevDay = ist_today - datetime.timedelta(days=1)
    return str(ist_today.strftime('%Y-%m-%d')), str(ist_prevDay.strftime('%Y-%m-%d'))


def message_handler(data, candle_response, volume_response, technical_response, sr_response):
    t = PrettyTable(['Bullish', candle_response['candle_stick']['stock_id']])
    t.add_row(['Quantity       ', math.ceil(amountPerStock / data['close'][-1])])
    t.add_row(['Buy       ', round(data['close'][-1], 2)])
    t.add_row(['StopLoss  ', round(data['low'][-1], 2)])
    t.add_row(['Candle    ', candle_response['candle_stick']['pattern']])
    t.add_row(['Technical ', technical_response['technical_indicator']["pattern"]])
    t.add_row(['SR        ', sr_response['sr_indicator']["pattern"]])
    t.add_row(['SR_Value  ', round(sr_response['sr_indicator']["level"], 2)])
    return t


def telegram_notification(message):
    response = requests.post("https://api.telegram.org/bot1898967363:AAFKsxIHb3HlCkLl7SZcM8FcSS2tP0llmlc/sendMessage",
                             params={'chat_id': '-544542415', 'text': message})


def main():
    Report = []
    for stock_id, stock_name in Stock.items():
        try:
            print(count, end='\r\n')
            data = yf.Ticker(str(stock_id) + '.NS').history(period='1y')
            #data = yf.Ticker(str(stock_id) + '.NS').history(start='2020-07-21', end='2021-07-22')
            data.columns = ['open', 'high', 'low', 'close', 'Volume', 'Dividends', 'Stock Splits']
            candle_response = brain_candle.candle_stick(data, stock_id, stock_name)
            volume_response = volume_indicator.volume_indicate(data, stock_id, stock_name)
            technical_response = technical_indicator.technical_indicate(data, stock_id, stock_name)
            sr_response = sr_indicator.sr_indicate(data, stock_id, stock_name)
            count += 1
            if candle_response['candle_stick']['indicator'] and volume_response['volume_indicator']['indicator'] and \
                    technical_response['technical_indicator']["indicator"] and sr_response['sr_indicator']["indicator"]:
                candle_stick += 1
                Report.append([stock_id, stock_name, data['close'][-1]])
                print('{} - {}'.format(stock_id, stock_name))
                message = message_handler(data, candle_response, volume_response, technical_response, sr_response)
                telegram_notification(message)
        except Exception as e:
            print(e)
    today, prevDay = get_filenames()
    try:
        Report_Data = pd.DataFrame(Report, index=None)
        Report_Data.columns = ['Stock_ID', 'Stock_Name', 'Close Price']
        Report_Data.sort_values('Close Price', inplace=True)
        Report_Data.to_csv('/Users/jyotijen/Desktop/StockRecommend/' + today + '.csv')
        #handler.performance_calculate(today, amountPerStock)
    except Exception as e:
        print(e)
