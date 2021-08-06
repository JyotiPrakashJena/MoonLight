from candlestick import candlestick as cs


def detect_pattern(data):
    data = cs.piercing_pattern(data, target='result')
    return data['result'][-1]