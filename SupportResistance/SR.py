import numpy as np
import math


def isSupport(df, i):
    return df['low'][i] < df['low'][i - 1] < df['low'][i - 2] and df['low'][i] < df['low'][i + 1] < df['low'][i + 2]


def isResistance(df, i):
    return df['high'][i] > df['high'][i - 1] and df['high'][i] > df['high'][i + 1] > df['high'][i + 2] and df['high'][
        i - 1] > df['high'][i - 2]


def isFarFromLevel(l, s, levels):
    return np.sum([abs(l - x) < s for x in levels]) == 0


def price_validation(data, levels):
    low = data['low'][-1]
    for level in levels:
        if math.isclose(low, level, abs_tol=low * 0.005):
            return True, level
    return False, 0


def sr_indicator(data):
    levels = []
    s = np.mean(data['high'] - data['low'])
    for i in range(2, data.shape[0] - 2):
        if isSupport(data, i):
            l = data['low'][i]
            if isFarFromLevel(l, s, levels):
                levels.append(l)
        elif isResistance(data, i):
            l = data['high'][i]
            if isFarFromLevel(l, s, levels):
                levels.append(l)
    # indicator, sr = price_validation(data, levels)
    return price_validation(data, levels)
