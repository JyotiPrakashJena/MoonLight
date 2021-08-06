import math


def price_validation(data, levels):
    low = data['low'][-1]
    for level in levels:
        if math.isclose(low, level, abs_tol=low * 0.005):
            return True, level
    return False, 0


def fibo_indicator(data):
    highest_swing = -1
    lowest_swing = -1
    for i in range(1, data.shape[0] - 1):
        if data['high'][i] > data['high'][i - 1] and data['high'][i] > data['high'][i + 1] and (
                highest_swing == -1 or data['high'][i] > data['high'][highest_swing]):
            highest_swing = i
        if data['low'][i] < data['low'][i - 1] and data['low'][i] < data['low'][i + 1] and (
                lowest_swing == -1 or data['low'][i] < data['low'][lowest_swing]):
            lowest_swing = i

    ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    levels = []
    max_level = data['high'][highest_swing]
    min_level = data['low'][lowest_swing]
    for ratio in ratios:
        if highest_swing > lowest_swing:  # Uptrend
            levels.append(max_level - (max_level - min_level) * ratio)
        else:  # Downtrend
            levels.append(min_level + (max_level - min_level) * ratio)
    return price_validation(data, levels)
