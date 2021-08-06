from candlestick import candlestick as cs


def detect_pattern(data):
    data = cs.hammer(data, target='result')
    return data['result'][-1]
