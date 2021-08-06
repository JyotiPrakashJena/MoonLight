
def detect_pattern(data):
    fiftyEMA = data.close.ewm(span=12, adjust=False).mean()
    return data['close'][-1] > fiftyEMA[-1]  # Current M.P is greater than 50days EMA

