from statistics import mean


def avgBody(Open, Close):
    return mean(abs(x - y) for x, y in zip(Open, Close))


def ratio(a, b):
    return abs(round((a - b) / a, 2)) if a != 0 else 0


def detect_pattern(data):
    current = data.iloc[-1]
    prev = data.iloc[-2]
    realbody = abs(current['open'] - current['close'])
    return ratio(current['open'], current['low']) < 0.0015 and ratio(current['high'],
                                                                                     current[
                                                                                         'close']) < 0.0015 and realbody >= avgBody(
        data['open'], data['close'])
