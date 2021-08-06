from statistics import mean


def response_handler(stock_id, stock_name, indicator):
    response = {'volume_indicator': {'stock_id': 'na', 'stock_name': 'na', 'indicator': False}}
    response['volume_indicator']['stock_id'] = stock_id
    response['volume_indicator']['stock_name'] = stock_name
    response['volume_indicator']["indicator"] = indicator
    return response


def volume_indicate(data, stock_id, stock_name):
    avgVolume = mean(data['Volume'][:-1])
    if avgVolume >= data['Volume'][-1]:
        return response_handler(stock_id, stock_name, True)
    return response_handler(stock_id, stock_name, False)
