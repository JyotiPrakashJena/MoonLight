from candlestick import candlestick as cs


def detect_pattern(data):
    data = cs.bullish_engulfing(data, target='result')
    return data['result'][-1]
