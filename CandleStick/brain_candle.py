from . import BullEngulf,BullHarami,BullPinBar,Hammer,Marubozu,MorningStar,Piercing


"""
{'candle_stick':{'trend':'Bullish','stock_id':'stock_id','stock_name':'stock_name','pattern':'Bullish Engulf','indicator':False}}
"""


def response_handler(stock_id, stock_name, pattern, indicator):
    response = {'candle_stick': {'trend': 'Bullish', 'stock_id': 'na', 'stock_name': 'na',
                                 'pattern': 'na', 'indicator': False}}
    response['candle_stick']['stock_id'] = stock_id
    response['candle_stick']['stock_name'] = stock_name
    response['candle_stick']['pattern'] = pattern
    response['candle_stick']["indicator"] = indicator
    return response


def candle_stick(data, stock_id, stock_name):
    if len(data) > 2:
        if BullEngulf.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Bullish Engulf', True)
        elif BullHarami.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Bullish Harami', True)
        elif BullPinBar.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Bullish PinBar', True)
        elif Hammer.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Bullish Hammer', True)
        elif Marubozu.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Bullish Marubozu', True)
        elif MorningStar.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Morning Star', True)
        elif Piercing.detect_pattern(data):
            return response_handler(stock_id, stock_name, 'Piercing', True)
    return response_handler(stock_id, stock_name, 'No Pattern', False)
