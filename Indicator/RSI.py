import yfinance as yf


def detect_pattern(data):
    RSI_Threshold = 25
    delta = data.close.diff()
    window = 15
    up_days = delta.copy()
    up_days[delta <= 0] = 0.0
    down_days = abs(delta.copy())
    down_days[delta > 0] = 0.0
    RS_up = up_days.rolling(window).mean()
    RS_down = down_days.rolling(window).mean()
    rsi = 100 - 100 / (1 + RS_up / RS_down)
    return rsi[-1] <= RSI_Threshold
