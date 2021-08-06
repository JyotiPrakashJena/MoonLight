from candlestick import candlestick as cs


def detect_pattern(data):
    data = cs.morning_star(data, target='result')
    return data['result'][-1]
