def detect_pattern(data):
    fiftyEMA = data.close.ewm(span=50, adjust=False).mean()
    centEMA = data.close.ewm(span=50, adjust=False).mean()
    return fiftyEMA[-1] > centEMA[-1]  # 50days EMA is greater than 100days EMA
