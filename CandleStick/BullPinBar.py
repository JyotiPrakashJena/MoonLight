def detect_pattern(data):
    current = data.iloc[-1]
    prev = data.iloc[-2]
    realbody = abs(current['open'] - current['close'])
    candle_range = current['high'] - current['low']
    return realbody <= candle_range / 3 and min(current['open'], current['close']) > (
            current['high'] + current['low']) / 2 and current['low'] < prev['low']
