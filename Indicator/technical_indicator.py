from . import CrossMovingAvg, MACD, MovingAvg, RSI

"""
{'technical_indicator':{'trend':'Bullish','stock_id':'stock_id','stock_name':'stock_name','pattern':'Bullish Engulf','indicator':'True'}}
"""


def response_handler(stock_id, stock_name, pattern, indicator):
    response = {'technical_indicator': {'trend': 'Bullish', 'stock_id': 'na', 'stock_name': 'na',
                                        'pattern': 'na', 'indicator': False}}
    response['technical_indicator']['stock_id'] = stock_id
    response['technical_indicator']['stock_name'] = stock_name
    response['technical_indicator']['pattern'] = pattern
    response['technical_indicator']["indicator"] = indicator
    return response


def technical_indicate(data, stock_id, stock_name):
    if len(data) > 2:
        if RSI.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'RSI', True)
        elif MACD.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'MACD', True)
        elif CrossMovingAvg.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Cross Moving Average', True)
        elif MovingAvg.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Moving Average', True)

    return response_handler(stock_id, stock_name, 'No Pattern', False)
