def detect_pattern(data):
    exp1 = data.close.ewm(span=12, adjust=False).mean()
    exp2 = data.close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    return macd[-1] > exp3[-1]  # MACD greater than Signal Line
