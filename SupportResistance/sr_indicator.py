from . import SR,FiboLevels


def response_handler(stock_id, stock_name, pattern, level, indicator):
    response = {'sr_indicator': {'trend': 'Bullish', 'stock_id': 'na', 'stock_name': 'na',
                                 'pattern': 'na', 'level': 0, 'indicator': False}}
    response['sr_indicator']['stock_id'] = stock_id
    response['sr_indicator']['stock_name'] = stock_name
    response['sr_indicator']['pattern'] = pattern
    response['sr_indicator']['level'] = level
    response['sr_indicator']["indicator"] = indicator
    return response


def sr_indicate(data, stock_id, stock_name):

    indicator_sr, level_sr = FiboLevels.fibo_indicator(data)
    if indicator_sr:
        return response_handler(stock_id, stock_name, 'Fibonacci', level_sr, True)

    indicator_sr, level_sr = SR.sr_indicator(data)
    if indicator_sr:
        return response_handler(stock_id, stock_name, 'Support Resistance', level_sr, True)

    return response_handler(stock_id, stock_name, 'NA', 0, False)
