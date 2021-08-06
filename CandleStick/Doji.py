from candlestick import candlestick as cs


def detect_pattern(data):
    data = cs.doji(data, target='result')
    return data['result'][-1]
