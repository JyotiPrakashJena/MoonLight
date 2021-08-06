import pandas as pd
import yfinance as yf
import math
# from StockRecommender.main import telegram_notification
import os


def performance_calculate(filename, amountPerStock):
    data = pd.read_csv(filename + '.csv')
    # data = pd.read_csv(filename)
    Income = []
    SellPrice = []
    quantity = []
    StockId = []
    count = 0
    Performance = {}
    for index, row in data.iterrows():
        print(count)
        stockId = row['Stock ID']
        StockId.append(stockId)
        closePrice = row['Close Price']
        Quantity = math.ceil(amountPerStock / closePrice)
        recent_data = yf.Ticker(str(stockId) + '.NS').history(period='1d')
        recentClosePrice = recent_data['Close'][-1]
        diff = (recentClosePrice - closePrice)
        income = diff * 0.975 if diff > 0 else diff * 1.025
        SellPrice.append(recentClosePrice)
        quantity.append(Quantity)
        Income.append(round(income * Quantity, 2))
        print(round(income * Quantity, 2))
        count += 1
    Performance['Stock Id'] = StockId
    Performance['Quantity'] = quantity
    Performance['Income'] = Income
    # telegram_notification('Income {} on Invest of {}'.format(sum(Income), len(Income) * amountPerStock))
    # data.to_csv('/Users/jyotijen/Desktop/StockRecommend/' + 'Performance_' + filename + '.csv', index=None)
    if os.path.exists('/Users/jyotijen/Desktop/StockRecommend/' + filename + '.csv') and os.path.isfile(
            '/Users/jyotijen/Desktop/StockRecommend/' + filename + '.csv'):
        os.remove('/Users/jyotijen/Desktop/StockRecommend/' + filename + '.csv')
        print("file deleted")
    return pd.DataFrame(Performance, index=None), sum(Income), len(Income) * amountPerStock
